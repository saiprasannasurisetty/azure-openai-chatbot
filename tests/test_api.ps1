# Test script for the new API features

$baseUrl = "http://127.0.0.1:8080"

# Step 1: Generate API key
Write-Host "Step 1: Generating API key..." -ForegroundColor Green
$keyResponse = Invoke-WebRequest -Uri "$baseUrl/auth/generate-key" -Method POST
$keyData = $keyResponse.Content | ConvertFrom-Json
$apiKey = $keyData.api_key
Write-Host "API Key: $apiKey`n"

# Step 2: Test chat endpoint with authentication
Write-Host "Step 2: Testing /chat with authentication..." -ForegroundColor Green
$chatBody = @{ prompt = "What is Python?" } | ConvertTo-Json
$chatHeaders = @{
    "Authorization" = "Bearer $apiKey"
    "X-Session-ID" = "session-001"
}
$chatResponse = Invoke-WebRequest -Uri "$baseUrl/chat" -Method POST -ContentType "application/json" -Body $chatBody -Headers $chatHeaders
$chatData = $chatResponse.Content | ConvertFrom-Json
Write-Host "Response: $($chatData.response)`n"

# Step 3: Test persistent history
Write-Host "Step 3: Testing /history (persistent storage)..." -ForegroundColor Green
$historyHeaders = @{
    "Authorization" = "Bearer $apiKey"
    "X-Session-ID" = "session-001"
}
$historyResponse = Invoke-WebRequest -Uri "$baseUrl/history" -Method GET -Headers $historyHeaders
$historyData = $historyResponse.Content | ConvertFrom-Json
Write-Host "Total messages: $($historyData.total_messages)"
Write-Host "History:`n"
$historyData.history | Format-Table -AutoSize

# Step 4: Test rate limiting
Write-Host "`nStep 4: Testing rate limiting (first few requests)..." -ForegroundColor Green
$rateLimitHeaders = @{
    "Authorization" = "Bearer $apiKey"
    "X-Session-ID" = "session-002"
}
for ($i = 1; $i -le 3; $i++) {
    $testBody = @{ prompt = "Test message $i" } | ConvertTo-Json
    $testResponse = Invoke-WebRequest -Uri "$baseUrl/chat" -Method POST -ContentType "application/json" -Body $testBody -Headers $rateLimitHeaders
    $testData = $testResponse.Content | ConvertFrom-Json
    Write-Host "Request $i successful - Session: $($testData.session_id)"
}

Write-Host "`nAll tests completed successfully!" -ForegroundColor Green
