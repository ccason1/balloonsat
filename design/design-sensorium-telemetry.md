# Bag of requirements

1. System should poll/interrogate I2C bus and identify available data sources, test them, and include into log line format. There may be multiple, including overlapping, log line formats. Formats will be coded and code starting the line.  
2. Available data sources should be listed and, later, have a cmd-line selector app for confirmation. Default is all identified into one line.
3. Data source database should have all sources described in detail.
4. Each source should be quantized and compressed to save room in telemetry messages. Hex or base-64 integers can save a lot of room. The codec should be available on both sides of the telemetry link.
