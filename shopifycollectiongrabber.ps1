$headers = @{
    "X-Shopify-Access-Token" = "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"
}

$url = "https://suppliesforblacksmiths.com/admin/api/2023-10/smart_collections.json"

function Get-ShopifyData {
    param(
        [string]$Url
    )

    $allCollections = @()

    do {
        try {
            Write-Host "Requesting URL: $Url"
            $response = Invoke-WebRequest -Uri $Url -Method Get -Headers $headers
            $data = $response.Content | ConvertFrom-Json
            $allCollections += $data.smart_collections | ForEach-Object {
                [PSCustomObject]@{
                    ID = $_.id
                    Handle = $_.handle
                }
            }
            
            # Extract next page URL from Link header
            $linkHeader = $response.Headers.Link
            if ($linkHeader -and $linkHeader -match '<(https://[^>]+)>;\s*rel="next"') {
                $Url = $matches[1]
            }
            else {
                $Url = $null
            }
        }
        catch {
            Write-Host "Error: $($_.Exception.Message)"
            if ($_.Exception.Response) {
                Write-Host "Response Status Code: $($_.Exception.Response.StatusCode.Value__) - $($_.Exception.Response.StatusDescription)"
                Write-Host "Response Headers: $($_.Exception.Response.Headers)"
            }
            $Url = $null
        }
    } while ($Url)

    return $allCollections
}

# Fetch all data
$collections = Get-ShopifyData -Url $url

# Output data to CSV file
$outputFile = "Shopify_Collections.csv"
$collections | Export-Csv -Path $outputFile -NoTypeInformation

Write-Host "Data exported to $outputFile successfully."
