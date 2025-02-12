OUTPUT_FILE="nav_data.tsv"

# Fetch data from the URL
URL="https://www.amfiindia.com/spages/NAVAll.txt"

# Download and process the data
curl -s "$URL" | awk -F';' 'BEGIN { print "Scheme Name\tAsset Value" } NF > 1 { print $4 "\t" $5 }' > "$OUTPUT_FILE"
