$Start = [int](Get-Content ".\_make_range.txt" -TotalCount 1).Trim()

$Files = @(
	".\all_results_a.txt",
	".\all_results_b.txt"
)

foreach ($File in $Files) {
	if (!(Test-Path $File)) {
		continue
	}

	$Lines = Get-Content $File
	$KeepCount = $Lines.Count

	for ($i = 0; $i -lt $Lines.Count; $i++) {
		if ($Lines[$i] -match '===== .*_H(\d+)\.exe =====') {
			$Version = [int]$Matches[1]

			if ($Version -ge $Start) {
				$KeepCount = $i
				break
			}
		}
	}

	if ($KeepCount -eq 0) {
		[System.IO.File]::WriteAllText(
			$File,
			"",
			(New-Object System.Text.UTF8Encoding($false))
		)
	} elseif ($KeepCount -lt $Lines.Count) {
		$KeepLines = $Lines[0..($KeepCount - 1)]
		[System.IO.File]::WriteAllLines(
			$File,
			$KeepLines,
			(New-Object System.Text.UTF8Encoding($false))
		)
	}
}