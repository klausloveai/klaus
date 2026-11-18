const fs=require('node:fs'),path=require('node:path'),os=require('node:os'),crypto=require('node:crypto'),{spawn}=require('node:child_process');
if(Number(process.versions.node.split('.')[0])<18)throw Error('Use an existing Node 18+ runtime; no software is installed by this tool.');
const args=process.argv.slice(2);let output,origin='https://api.chatcut.io';
for(let i=0;i<args.length;i++){if(args[i]==='--output')output=args[++i];else if(args[i]==='--fixture-origin'){const u=new URL(args[++i]);if(u.protocol!=='http:'||u.hostname!=='127.0.0.1'||u.pathname!=='/'||u.search||u.hash||u.username||u.password)throw Error('Only loopback HTTP is accepted as a fixture origin');origin=u.origin;}else throw Error('Unknown option: '+args[i]);}
const uuid=crypto.randomUUID();
output=path.resolve(output??path.join(os.tmpdir(),'chatcut-framing-'+new Date().toISOString().replace(/[:.]/g,'-')+'-'+uuid.slice(0,8)));
const json=(file,data)=>fs.writeFileSync(path.join(output,file),JSON.stringify(data,null,2),{mode:0o600});
const names=['date','content-type','content-length','transfer-encoding','content-encoding','connection','www-authenticate','x-request-id','x-amzn-trace-id'];
const run=argv=>new Promise(resolve=>{
  const child=spawn('curl.exe',argv,{windowsHide:true,stdio:['ignore','pipe','pipe']});const stdout=[],stderr=[];let outBytes=0,errBytes=0,limited=false,error;
  const timer=setTimeout(()=>{error={code:'CHILD_TIMEOUT',message:'curl child exceeded 12000ms'};child.kill();},12000);
  child.stdout.on('data',b=>{outBytes+=b.length;if(outBytes<=262144)stdout.push(b);else{limited=true;error={code:'METRICS_LIMIT',message:'curl metrics exceeded 256KiB'};child.kill();}});
  child.stderr.on('data',b=>{errBytes+=b.length;if(errBytes<=131072)stderr.push(b);else{limited=true;error={code:'STDERR_LIMIT',message:'curl stderr exceeded 128KiB; source error incomplete'};child.kill();}});
  child.once('error',e=>{error={name:e.name,message:e.message,code:e.code};});
  child.once('close',(code,signal)=>{clearTimeout(timer);resolve({code,signal,stdout:Buffer.concat(stdout),stderr:Buffer.concat(stderr),error,limited,outBytes,errBytes});});
});
(async()=>{
  const version=await run(['--disable','--version']);const versionLine=version.stdout.toString('utf8').split(/\r?\n/)[0];const match=versionLine.match(/^curl (\d+)\.(\d+)\.(\d+)/);
  if(version.code!==0||!match||Number(match[1])<8||(Number(match[1])===8&&Number(match[2])<4))throw Error('Existing curl.exe 8.4+ required to bound unknown-size downloads; no network requests sent. '+(version.error?.message??''));
  fs.mkdirSync(output,{mode:0o700});
  const start=new Date();json('anonymous-initialize.json',{jsonrpc:'2.0',id:uuid,method:'initialize',params:{protocolVersion:'2025-11-25',capabilities:{},clientInfo:{name:'chatcut-framing-public-check',version:'1'}}});
  const requests=[{name:'entry',method:'POST',path:'/api/external-mcp/mcp'},{name:'scoped',method:'GET',path:'/.well-known/oauth-protected-resource/api/external-mcp/mcp'},{name:'root',method:'GET',path:'/.well-known/oauth-protected-resource'}],rows=[];
  const format='%{json}\nCHATCUT_SELECTED_HEADERS\nHTTP/%{http_version} %{response_code}\r\n'+names.map(n=>n+': %header{'+n+'}\r\n').join('');
  for(const item of requests){
    const argv=['--disable','--silent','--show-error','--http1.1','--raw','--connect-timeout','5','--max-time','10','--max-filesize','131072','--request',item.method,'--header','Accept: application/json','--header','Accept-Encoding: identity','--header','Connection: close','--header','X-ChatCut-Diagnostic-ID: '+uuid,'--header','X-ChatCut-MCP-Client: framing-public-check-20261028','--output',path.join(output,item.name+'.body.raw'),'--write-out',format];
    if(item.method==='POST')argv.push('--header','Content-Type: application/json','--data-binary','@'+path.join(output,'anonymous-initialize.json'));
    argv.push(origin+item.path);const startedAt=new Date().toISOString();const result=await run(argv);const completedAt=new Date().toISOString();
    const [metricsText,headerText='']=result.stdout.toString('utf8').split('CHATCUT_SELECTED_HEADERS',2);fs.writeFileSync(path.join(output,item.name+'.metrics-private.json'),metricsText.trim(),{mode:0o600});fs.writeFileSync(path.join(output,item.name+'.stderr.txt'),result.stderr,{mode:0o600});
    let metrics={};try{metrics=JSON.parse(metricsText);}catch{}const headers={},selected=[];
    for(const line of headerText.trim().split(/\r?\n/)){if(line.startsWith('HTTP/'))selected.push(line);else{const at=line.indexOf(':');if(at>=0){const key=line.slice(0,at).toLowerCase(),value=line.slice(at+1).trim();if(names.includes(key)&&value){headers[key]=value;selected.push(key+': '+value);}}}}
    fs.writeFileSync(path.join(output,item.name+'.headers.txt'),selected.join('\r\n')+'\r\n\r\n',{mode:0o600});
    rows.push({...item,startedAt,completedAt,curlExitCode:result.code,childSignal:result.signal,childError:result.error??null,metricsOrErrorLimited:result.limited,responseStatus:metrics.response_code??null,httpVersion:metrics.http_version??null,remoteIp:metrics.remote_ip??null,sslVerifyResult:metrics.ssl_verify_result??null,proxyUsed:metrics.proxy_used??null,peerIssuer:metrics.certs?.match(/^Issuer:(.*)$/m)?.[1]?.trim()??null,headers,responseHeadersFile:item.name+'.headers.txt',responseBodyFile:item.name+'.body.raw',stderrFile:item.name+'.stderr.txt'});
  }
  const end=new Date();json('capture.json',{schemaVersion:1,diagnosticId:uuid,origin,startedAt:start.toISOString(),completedAt:end.toISOString(),kind:'later_independent_public_probe_not_original_host_request',requestCount:3,credentialsSent:false,loginAttempted:false,uploaded:false,tlsVerificationDisabled:false,curlrcLoaded:false,credentialHeadersCaptured:false,setCookieCaptured:false,headerCapture:'selected framing and correlation values via curl write-out; not complete header wire octets',route:'curl_http11_existing_proxy_environment_and_system_TLS_trust; not_native_host_route',proxyEnvironmentPresent:Object.fromEntries(['HTTP_PROXY','HTTPS_PROXY','ALL_PROXY','NO_PROXY'].map(n=>[n,!!process.env[n]])),curlVersion:versionLine,nodeVersion:process.version,rows});
  const serverDates=rows.map(r=>Date.parse(r.headers.date)).filter(Number.isFinite),queryStart=new Date((serverDates.length?Math.min(...serverDates):start.getTime())-30000),queryEnd=new Date((serverDates.length?Math.max(...serverDates):end.getTime())+30000);
  json('server-query.json',[{name:'paired-public-framing',start:queryStart.toISOString(),end:queryEnd.toISOString(),timeBasis:serverDates.length?'response Date headers; verify alongside local UTC times':'local UTC fallback',query:"['chatcut-logs'] | where stage == 'production' and (eventName startswith 'GET /.well-known/' or eventName == 'POST /api/external-mcp/mcp') | extend d=coalesce(attributes.mcpDiagnostics,parse_json(attributesJson).mcpDiagnostics) | where tostring(d.request.diagnosticId) == '"+uuid+"' | project _time,eventName,requestId,nodeId,commitSha,service,statusCode,outcome,errorMessage,errorType,d | sort by _time asc | take 12"}]);
  json('files.sha256.json',fs.readdirSync(output).map(file=>({file,bytes:fs.statSync(path.join(output,file)).size,sha256:crypto.createHash('sha256').update(fs.readFileSync(path.join(output,file))).digest('hex')})));
  console.log(JSON.stringify({output,diagnosticId:uuid,requests:3,login:false,upload:false,credentialsCaptured:false,setCookieCaptured:false,rows:rows.map(r=>({name:r.name,status:r.responseStatus,curlExitCode:r.curlExitCode,requestId:r.headers['x-request-id']}))},null,2));
})().catch(e=>{console.error(e.message);process.exitCode=1;});
