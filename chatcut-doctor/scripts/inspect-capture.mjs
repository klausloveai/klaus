import fs from 'node:fs';
import path from 'node:path';
import {createHash} from 'node:crypto';
const folder=path.resolve(process.argv[2]??'.');
const serverFile=process.argv[3];
const receipt=JSON.parse(fs.readFileSync(path.join(folder,'capture.json'),'utf8').replace(/^\uFEFF/,''));
const server=serverFile?JSON.parse(fs.readFileSync(serverFile,'utf8').replace(/^\uFEFF/,'')):null;
const sha=b=>createHash('sha256').update(b).digest('hex');
const readText=file=>{const b=fs.readFileSync(file);return b[0]===0xff&&b[1]===0xfe?b.subarray(2).toString('utf16le'):b.toString('utf8').replace(/^\uFEFF/,'');};
function frame(headers,body,exit){
  const te=headers['transfer-encoding']?.toLowerCase().split(',').map(x=>x.trim());
  const fail=reason=>({state:'invalid',reason});
  if(te&&headers['content-length']!==undefined)return fail('both_transfer_encoding_and_content_length');
  if(te?.at(-1)==='chunked'){
    let at=0;const chunks=[];
    while(at<body.length){
      const end=body.indexOf('\r\n',at);
      if(end<0)return body[at]!==undefined&&!/[0-9a-f]/i.test(String.fromCharCode(body[at]))?fail('invalid_chunk_size'):{state:'incomplete',reason:'chunk_size_not_complete'};
      const line=body.subarray(at,end).toString('latin1').split(';')[0];
      if(!/^[0-9a-f]+$/i.test(line))return fail('invalid_chunk_size');
      const n=parseInt(line,16);at=end+2;
      if(!Number.isSafeInteger(n)||n>131072)return {state:'incomplete',reason:'chunk_exceeds_capture_limit'};
      if(n===0){
        const trailerEnd=body.subarray(at,at+2).equals(Buffer.from('\r\n'))?at+2:(body.indexOf('\r\n\r\n',at)>=0?body.indexOf('\r\n\r\n',at)+4:null);
        if(trailerEnd===null)return {state:'incomplete',reason:'terminal_trailers_not_complete'};
        if(trailerEnd!==body.length)return fail('bytes_after_terminal_chunk');
        const decoded=Buffer.concat(chunks);return {state:'valid',coding:'chunked',decodedBytes:decoded.length,decodedSha256:sha(decoded)};
      }
      if(at+n+2>body.length)return {state:'incomplete',reason:'chunk_not_complete'};
      chunks.push(body.subarray(at,at+n));at+=n;
      if(!body.subarray(at,at+2).equals(Buffer.from('\r\n')))return fail('missing_chunk_terminator');at+=2;
    }
    return {state:'incomplete',reason:'terminal_chunk_missing'};
  }
  if(te)return {state:'incomplete',reason:'unsupported_transfer_encoding'};
  if(headers['content-length']!==undefined){
    if(!/^\d+$/.test(headers['content-length']))return fail('invalid_content_length');
    const expected=Number(headers['content-length']);
    if(body.length>expected)return fail('content_length_exceeded');
    if(body.length<expected)return {state:'incomplete',reason:'content_length_not_complete'};
    return {state:'valid',coding:'content-length',decodedBytes:body.length,decodedSha256:sha(body)};
  }
  return exit===0?{state:'valid',coding:'close',decodedBytes:body.length,decodedSha256:sha(body)}:{state:'incomplete',reason:'close_delimited_body_not_complete'};
}
const rows=receipt.rows.map(row=>{
  const h=fs.readFileSync(path.join(folder,row.responseHeadersFile),'latin1');
  const final=h.split(/\r?\n\r?\n/).filter(x=>/^HTTP\/\S+ \d{3}/.test(x)).at(-1);
  const headers={};for(const line of final?.split(/\r?\n/).slice(1)??[]){const at=line.indexOf(':');if(at>=0){const k=line.slice(0,at).toLowerCase();const v=line.slice(at+1).trim();headers[k]=headers[k]===undefined?v:headers[k]+','+v;}}
  const bodyFile=path.join(folder,row.responseBodyFile),body=fs.existsSync(bodyFile)?fs.readFileSync(bodyFile):Buffer.alloc(0);
  let rawBodyJsonValid=false;try{JSON.parse(body.toString('utf8'));rawBodyJsonValid=true;}catch{}
  let framing=final?frame(headers,body,row.curlExitCode):{state:'not_observed',reason:'no_http_response'};
  if(framing.state==='valid'&&row.curlExitCode!==0)framing={state:'incomplete',reason:'curl_failed_while_selected_framing_looks_complete',selectedFraming:framing};
  const matched=server?.rows?.filter(r=>r.d?.request?.diagnosticId===receipt.diagnosticId&&String(r.requestId)===headers['x-request-id']&&r.eventName===row.method+' '+row.path)??[];
  const origin=server?.data?.status?.isPartial===false&&matched.length===1?matched[0]:null;
  const app=origin?.d?.metadataResponse;
  return {name:row.name,method:row.method,path:row.path,status:row.responseStatus,curlExitCode:row.curlExitCode,framing,firstRawBodyByteHex:body.subarray(0,1).toString('hex'),rawBodyBytes:body.length,rawBodySha256:sha(body),rawBodyJsonValid,responseHeaders:Object.fromEntries(['content-type','content-length','transfer-encoding','connection','www-authenticate','x-request-id'].flatMap(k=>headers[k]===undefined?[]:[[k,headers[k]]])),peerIssuer:row.peerIssuer,serverPair:origin?{match:'diagnostic_id_query_plus_request_id_and_route',time:origin._time,nodeId:origin.nodeId,commitSha:origin.commitSha,applicationObservation:app??null,rawJsonHashEqualsApplicationBody:!!app&&rawBodyJsonValid&&sha(body)===app.bodySha256,decodedHashEqualsApplicationBody:!!app&&framing.decodedSha256===app.bodySha256,limitation:'application record is before Node HTTP framing; not server egress wire'}:{match:'unconfirmed',candidateCount:matched.length},stderr:readText(path.join(folder,row.stderrFile))};
});
const output={analyzedAt:new Date().toISOString(),diagnosticId:receipt.diagnosticId,kind:receipt.kind,serverResultPartial:server?.data?.status?.isPartial??null,rows,limits:['Independent public requests do not recover or identify the original native failure','Only complete framing is marked valid; capture limits and transport errors remain explicit','Application body hashes do not establish post-framing Node, ALB, or local inspection output']};
fs.writeFileSync(path.join(folder,'analysis.json'),JSON.stringify(output,null,2));
console.log(JSON.stringify(rows.map(x=>({name:x.name,status:x.status,curlExitCode:x.curlExitCode,framing:x.framing.state,reason:x.framing.reason,requestId:x.responseHeaders['x-request-id'],serverPair:x.serverPair.match})),null,2));
