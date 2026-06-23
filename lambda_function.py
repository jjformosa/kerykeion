import os
import json
from kerykeion import AstrologicalSubject, KerykeionChartSVG
import boto3

def handler(event, context):
    
    try:
        # Process DynamoDB Stream records
        for record in event.get('Records', []):
            # Ensure it's a DynamoDB record
            if record['eventSource'] != 'aws:dynamodb':
                continue

            # Get the new image (data after the change)
            # If you need the old image, use record['dynamodb']['OldImage']
            if 'NewImage' in record['dynamodb']:
                dynamodb_data = record['dynamodb']['NewImage']
                print(dynamodb_data)
                __type = dynamodb_data['__typename']['S']
                if __type != 'Profile':
                    continue
                birthInfo = dynamodb_data['birthInfo']['M']
                # Extract values from DynamoDB record
                # Note: DynamoDB streams return data with type descriptors
                birth_date = birthInfo['birthDay']['S']
                birth_time = birthInfo.get('birthTime', {}).get('S', '00:00')
                birth_long = birthInfo.get('birthLon', {}).get('N', '120.982025')
                birth_lat = birthInfo.get('birthLat', {}).get('N', '23.973875')
                birth_timeZone = birthInfo.get('birthTimeZone', {}).get('S', 'Asia/Taipei')
                file_name = dynamodb_data['awsCognitoId']['S']

                # Split birth date into components
                year, month, day = map(int, birth_date.split('/'))
                hour, minute = map(int, birth_time.split(':'))

                print(file_name)
                print(year)
                print(month)
                print(day)
                print(hour)
                print(minute)
                
                # Create astrological subject
                person = AstrologicalSubject(
                    file_name,
                    year,
                    month,
                    day,
                    hour,
                    minute,
                    lng=float(birth_long),
                    lat=float(birth_lat),
                    tz_str=birth_timeZone
                )
                
                # Make SVG chart
                synastry_chart = KerykeionChartSVG(person, new_output_directory="/tmp", chart_language="CN")
                synastry_chart.makeSVG()

                # Read file to memory
                with open(f"/tmp/{file_name} - Natal Chart.svg", "r") as f:
                    svg_content = f.read()
                
                # upload svg to s3
                bucket_name = os.environ['ASTROLOGY_CHART_BUCKET']
                s3 = boto3.client('s3')
                s3_upload = s3.put_object(
                    Bucket=bucket_name,
                    Key=f'astrology/{file_name}/astrology.svg',
                    Body=svg_content,
                    ContentType='image/svg+xml'
                )
                
                return {
                    'statusCode': 200,
                    'body': json.dumps({'message': 'SVG uploaded to S3 successfully'})
                }
        
        return {
            'statusCode': 400,
            'body': json.dumps({'message': 'No records to process'})
        }
        
    except Exception as e:
        import sys
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)
        return {
            'statusCode': 500,
            'body': json.dumps({'error': 'Internal server error'})
        }
