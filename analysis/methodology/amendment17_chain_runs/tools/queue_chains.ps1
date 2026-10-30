# Launch queued chains as running ones finish, keeping at most $Max chains (python interpreter pairs) alive.
# Each chain is started via WMI (survives harness task-tree kills), hidden, with --resume.
param([int]$Max = 14)
$root = "C:\Users\email\Documents\Claude\Projects\Electoral Boundary Analysis\alberta_audit"
$py = "C:\Users\email\.venvs\audit-k91\Scripts\python.exe"
$queue = [System.Collections.Generic.Queue[object]]::new()
foreach ($q in @(
  @{k=91;i=244;set="muni"}, @{k=91;i=245;set="muni"}, @{k=89;i=140;set="muni"}, @{k=89;i=141;set="muni"},
  @{k=91;i=234;set="eps25"}, @{k=91;i=235;set="eps25"}, @{k=89;i=132;set="eps25"}, @{k=89;i=133;set="eps25"},
  @{k=91;i=236;set="eps25"}, @{k=91;i=237;set="eps25"})) { $queue.Enqueue($q) }
$startup = New-CimInstance -ClassName Win32_ProcessStartup -ClientOnly -Property @{ShowWindow=[uint16]0}
function Running { @(Get-CimInstance Win32_Process -Filter "Name='python.exe'" | Where-Object CommandLine -like '*close_seats_ensemble*').Count / 2 }
while ($queue.Count -gt 0) {
  if ((Running) -lt $Max) {
    $j = $queue.Dequeue()
    $flags = if ($j.set -eq "muni") { "--proposal-eps 0.25 --muni-surcharge 0.5" } else { "--proposal-eps 0.25" }
    $d = "data\simulation_checkpoints_k$($j.k)_$($j.set)"; $n = $j.i
    New-Item -ItemType Directory -Force "$root\$d" | Out-Null
    $cmd = "cmd.exe /c `"`"$py`" -u analysis\scripts\close_seats_ensemble.py nk --k $($j.k) --idx $n --steps 252500 --chunk 500 $flags --resume --out $d\chain${n}_samples.csv > $d\chain$n.log 2> $d\chain$n.err`""
    $r = Invoke-CimMethod -ClassName Win32_Process -MethodName Create -Arguments @{CommandLine=$cmd; CurrentDirectory=$root; ProcessStartupInformation=$startup}
    "{0:HH:mm:ss} launched {1} k{2} idx{3} rc={4}" -f (Get-Date), $j.set, $j.k, $n, $r.ReturnValue
    Start-Sleep 20
  } else { Start-Sleep 30 }
}
"{0:HH:mm:ss} queue empty" -f (Get-Date)
