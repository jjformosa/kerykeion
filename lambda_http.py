def handler(event, context):
    import json
    from kerykeion import AstrologicalSubject, KerykeionChartSVG
    import request
    
    try:
        # Parse event body
        event_body = json.loads(event['body'])
        
        # Extract required fields with validation
        required_fields = ['fileName' 'birthDate']
        # 'birthTime', 'birthLong', 'birthLat'

        # Validate all required fields are present
        missing_fields = [field for field in required_fields if field not in event_body]
        if missing_fields:
            return {
                'statusCode': 400,
                'body': json.dumps({
                    'error': 'Missing required fields',
                    'missing_fields': missing_fields
                })
            }
            
        # Extract values from event body
        birth_date = event_body['birthDate']      # Expected format: "YYYY-MM-DD"
        birth_time = event_body.get('birthTime', '00:00')      # Expected format: "HH:MM"
        birth_long = event_body.get('birthLong', 0)
        birth_lat = event_body('birthLat', 0)
        # birth_location = event_body['birthLocation']

        # get geoInfo/TZInfo by location
        # use Google TimeZone API to fetch timeZoneInfo by lng lat
        
        
        # Split birth date into components
        year, month, day = map(int, birth_date.split('-'))
        hour, minute = map(int, birth_time.split(':'))
        
        # Create astrological subject
        person = AstrologicalSubject(
            fileName,
            year,
            month,
            day,
            hour,
            minute,
            lng=birth_long,
            lat=birth_lat,
            city=birth_location
        )
        
        # Get basic astrological information
        result = {
            'sun_sign': person.sun_sign,
            'moon_sign': person.moon_sign,
            'rising_sign': person.rising_sign,
            'positions': {
                planet: getattr(person, f"{planet}_position") 
                for planet in ['sun', 'moon', 'mercury', 'venus', 'mars']
            }
        }
        
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json'
            },
            'body': json.dumps(result)
        }
        
    except json.JSONDecodeError:
        return {
            'statusCode': 400,
            'body': json.dumps({'error': 'Invalid JSON in request body'})
        }
    except ValueError as e:
        return {
            'statusCode': 400,
            'body': json.dumps({'error': str(e)})
        }
    except Exception as e:
        print(e)
        return {
            'statusCode': 500,
            'body': json.dumps({'error': 'Internal server error'})
        }
