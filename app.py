from kerykeion import AstrologicalSubject, KerykeionChartSVG

first = AstrologicalSubject("菜胖", 1988, 12, 20, 6, 00, lng=121.5167, lat=25.05, tz_str="Asia/Taipei")
# Set the output directory to the current directory
synastry_chart = KerykeionChartSVG(first, new_output_directory=".", chart_language="CN")
synastry_chart.makeSVG()