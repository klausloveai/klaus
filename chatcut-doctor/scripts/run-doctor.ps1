param(
  [string]$Runtime,
  [string]$Context,
  [string]$Case,
  [string]$ResumeFile,
  [string]$Handoff,
  [string]$SourceEvent,
  [string]$UserData,
  [string]$EvidenceRef,
  [ValidateSet('check','repair','native-recheck','record-recheck','finish','status','upload','evidence','handoff')][string]$Action,
  [string]$ProjectId,
  [string]$Result,
  [string]$FailureRecord,
  [string]$CaseRoot
)
$ErrorActionPreference = 'Stop'
$doctorEntry = Join-Path $PSScriptRoot 'cli\bin\chatcut.mjs'
if (-not (Test-Path -LiteralPath $doctorEntry -PathType Leaf)) {
  throw 'This Skill needs the prepared local Doctor candidate. No global package was installed or substituted.'
}
if (-not $Runtime) {
  $doctorSelectedContext = $null
  if ($Context) {
    $doctorSelectedContext = Get-Content -LiteralPath $Context -Raw | ConvertFrom-Json
  } elseif ($Case) {
    $doctorSelectedContext = (Get-Content -LiteralPath (Join-Path $Case 'case.json') -Raw | ConvertFrom-Json).target
  } elseif ($ResumeFile -and (Test-Path -LiteralPath $ResumeFile -PathType Leaf)) {
    $doctorReference = Get-Content -LiteralPath $ResumeFile -Raw | ConvertFrom-Json
    $doctorSelectedContext = (Get-Content -LiteralPath (Join-Path $doctorReference.caseDir 'case.json') -Raw | ConvertFrom-Json).target
  }
  if ($doctorSelectedContext.surface -eq 'desktop' -and $doctorSelectedContext.launcher) {
    $doctorLauncherText = Get-Content -LiteralPath $doctorSelectedContext.launcher -Raw
    $doctorRuntimeMatch = [regex]::Match($doctorLauncherText, '(?m)^"([^"\r\n]+)" "[^"\r\n]+" %\*\r?$')
    if ($doctorRuntimeMatch.Success) { $Runtime = $doctorRuntimeMatch.Groups[1].Value }
  }
}
if (-not $Runtime) {
  $doctorRuntimeFile = Join-Path $PSScriptRoot 'runtime.json'
  if (Test-Path -LiteralPath $doctorRuntimeFile -PathType Leaf) {
    $Runtime = (Get-Content -LiteralPath $doctorRuntimeFile -Raw | ConvertFrom-Json).executable
  }
}
if (-not $Runtime) {
  $doctorNode = Get-Command node -CommandType Application -ErrorAction SilentlyContinue | Select-Object -First 1
  if ($doctorNode) { $Runtime = $doctorNode.Source }
}
if (-not $Runtime -or -not (Test-Path -LiteralPath $Runtime -PathType Leaf)) {
  throw 'Select an existing Node 22+ or ChatCut Electron executable with -Runtime. No runtime was downloaded and no app was opened.'
}
$doctorArguments = @($doctorEntry, 'doctor', '--json')
if ($Action) { $doctorArguments += @('--action', $Action) }
foreach ($doctorPair in @(@('--context',$Context), @('--case',$Case), @('--resume-file',$ResumeFile), @('--handoff',$Handoff), @('--source-event',$SourceEvent), @('--user-data',$UserData), @('--evidence-ref',$EvidenceRef), @('--project-id',$ProjectId), @('--result',$Result), @('--failure-record',$FailureRecord), @('--case-root',$CaseRoot))) {
  if ($doctorPair[1]) { $doctorArguments += @($doctorPair[0], $doctorPair[1]) }
}
$doctorPreviousNodeMode = $env:ELECTRON_RUN_AS_NODE
try {
  $env:ELECTRON_RUN_AS_NODE = '1'
  # A pipeline makes PowerShell wait for Electron's GUI-subsystem executable.
  $doctorRuntimeVersion = (& $Runtime -p 'process.versions.node' 2>&1 | Out-String).Trim()
  if ($LASTEXITCODE -ne 0 -or $doctorRuntimeVersion -notmatch '^([0-9]+)\.' -or [int]$Matches[1] -lt 22) {
    throw "The selected executable must provide Node 22+. Runtime returned: $doctorRuntimeVersion"
  }
  & $Runtime @doctorArguments | Write-Output
  exit $LASTEXITCODE
} finally {
  $env:ELECTRON_RUN_AS_NODE = $doctorPreviousNodeMode
}
