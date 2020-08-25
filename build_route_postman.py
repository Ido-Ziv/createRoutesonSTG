#!/usr/bin/env python
# -*- coding: utf-8 -*-
from datetime import datetime
import json

# # #
# SETTINGS
env = "stg"
time = "18:00 - 20:00"
force_today = True
date = "2020-08-12 10:00:00.000000"
force_premium = False
source = "300-deliveries.csv"
trigger_algo_wait_miliseconds = 1000 * 60 * 5
pr_events = [
    '''
    '''
]
te_events = [
    '''
pm.test("Status code is 201", function () {
    pm.response.to.have.status(201);
});
    ''',
]
trigger_timestamp = None  # None for current date
trigger_algo = True
# # #

trigger_timearg = trigger_timestamp if trigger_timestamp else datetime.now().strftime("%Y-%m-%dT12:30:00.000Z")

pr_events = [pr.replace('"', '\\"').replace('\n', '') for pr in pr_events]
te_events = [te.replace('"', '\\"').replace('\n', '') for te in te_events]

SDD_PICKUP_TIME_RANGES = (
    '07:00 - 10:00',
    '08:00 - 10:00',
    '09:00 - 11:00',
    '10:00 - 12:00',
    '11:00 - 13:00',
    '12:00 - 14:00',
    '13:00 - 15:00',
    '14:00 - 16:00',
    '15:00 - 17:00',
    '16:00 - 18:00',
)

# ToDO: If you change this constant - make sure about this function
#   delivery.helpers.get_nearest_time_ranges.
SDD_DROPOFF_TIME_RANGES = (
    '10:00 - 12:00',
    '11:00 - 13:00',
    '12:00 - 14:00',
    '12:00 - 15:00',
    '13:00 - 15:00',
    '14:00 - 16:00',
    '15:00 - 17:00',
    '16:00 - 18:00',
    '17:00 - 19:00',
    '18:00 - 21:00',
    '18:00 - 20:00',
    '19:00 - 21:00',
)

DELIVERY_TYPES = (
    'Envelope',
    'Small',
    'Medium',
    'Large'
)

CONFIRMATION_TYPES = (
    "sms",
    "sms",
    "photo",
    "signature"
)

api_keys = {
    "dev": "8dd00b85-5b30-4190-91bc-f374775610e2",
    "stg": "8dd00b85-5b30-4190-91bc-f374775610e2"
}

api_urls = {
    "dev": "https://dev-api.getpackage.com",
    "stg": "https://stg-api.getpackage.com",
}
new_api_urls = {
    "dev": "https://dev.getpackage-dev.com",
    "stg": "https://stg.getpackage-dev.com",
}

api_subdomains = {
    "dev": "dev-api",
    "stg": "stg-api"
}
new_api_subdomains = {
    "dev": "dev",
    "stg": "stg"
}

with open(f"postman_collection_generated.json", "w") as ostream:
    with open(source, "r", encoding="utf8") as istream:
        requests = []
        confirmation = 1
        for i, line in enumerate(istream.readlines()):
            delivery_id, pickup_date, is_same_day, sdd_pickup_time_range, sdd_dropoff_time_range, dropoff_confirmation, \
                delivery_type_id, sdd_package_id, spp_type, spp_required_secure, spp_instruction, spp_address, spp_full_name, spp_phone_number, \
                spd_type, spd_required_secure, spd_instruction, spd_address, spd_full_name, spd_phone_number = line.split("\t")

            pickup_date = date if not force_today else datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")

            #sdd_pickup_time_range = SDD_PICKUP_TIME_RANGES[int(sdd_pickup_time_range)]
            #sdd_dropoff_time_range = SDD_DROPOFF_TIME_RANGES[int(sdd_dropoff_time_range)]

            sdd_pickup_time_range = time
            sdd_dropoff_time_range = time
            delivery_type = DELIVERY_TYPES[int(delivery_type_id)-1]
            cid = confirmation
            dropoff_confirmation = CONFIRMATION_TYPES[cid]  # CONFIRMATION_TYPES[int(dropoff_confirmation)-1]
            confirmation += 1
            if confirmation > 3:
                confirmation = 1
            sdd_package_id = "{{$randomInt}}" * 3

            req = {
                "pickup_date": pickup_date,
                "is_same_day": is_same_day if not force_premium else False,
                "is_urgent": False,
                "pickup_time_range": sdd_pickup_time_range,
                "dropoff_time_range": sdd_dropoff_time_range,
                "confirmation": dropoff_confirmation,
                "item": {
                    "delivery_type": delivery_type, "package_id": sdd_package_id,
                },
                "returnable": True,
                "stop_points": [
                    {
                        "type": spp_type,
                        "required_secure": spp_required_secure,
                        "instruction": spp_instruction,
                        "location": {
                            "address": spp_address,
                            "country": "ישראל",
                        },
                        "contact": {
                            "full_name": spp_full_name,
                            "phone_number": spp_phone_number,
                        }
                    },
                    {
                        "type": spd_type,
                        "required_secure": spd_required_secure,
                        "instruction": spd_instruction,
                        "location": {
                            "address": spd_address,
                            "country": "ישראל",
                        },
                        "contact": {
                            "full_name": spd_full_name,
                            "phone_number": spd_phone_number,
                        }
                    }
                ]
            }

            raw = json.dumps(req)

            item = '''
                {
                    "name": "sdd-post-{delivery_id}",
                    "request": {
                        "method": "POST",
                        "header": [
                            {
                                "key": "Content-Type",
                                "value": "application/json",
                                "type": "text"
                            },
                            {
                                "key": "Authorization",
                                "value": "APIKEY {api_key}",
                                "description": "APIKEY 8567171b-0c9d-49a8-963e-30c6950c3380",
                                "type": "text"
                            }
                        ],
                        "body": {
                            "mode": "raw",
                            "raw": {raw}
                        },
                        "url": {
                            "raw": "{api_url}/api/v1/deliveries/",
                            "protocol": "https",
                            "host": [
                                "{api_subdomain}",
                                "getpackage",
                                "com"
                            ],
                            "path": [
                                "api",
                                "v1",
                                "deliveries",
                                ""
                            ]
                        }
                    },
                    "response": []
                }'''
            item = item.replace("{delivery_id}", delivery_id)
            item = item.replace("{raw}", json.dumps(raw))
            item = item.replace("{api_key}", api_keys[env])
            item = item.replace("{api_url}", api_urls[env])
            item = item.replace("{api_subdomain}", api_subdomains[env])
            requests.append(item)

        # Algo trigger
        if trigger_algo:
            item = '''
                {
                    "name": "trigger-algo",
                    "event": [
                        {
                            "listen": "prerequest",
                            "script": {
                                "id": "3fea43d7-5049-43c4-baba-207d9d3baaed",
                                "exec": [
                                    "setTimeout(function(){}, [{trigger_algo_wait_miliseconds}]);"
                                ],
                                "type": "text/javascript"
                            }
                        }
                    ],
                    "request": {
                        "method": "POST",
                        "header": [
                            {
                                "key": "Content-Type",
                                "value": "application/json",
                                "type": "text"
                            }
                        ],
                        "body": {
                            "mode": "raw",
                            "raw": "",
                            "options": {
                                "raw": {}
                            }
                        },
                        "url": {
                            "raw": "{new_api_url}/v1/deliveries/groups/0/{trigger_timestamp}/trigger",
                            "protocol": "https",
                            "host": [
                                "{new_api_subdomain}",
                                "getpackage-dev",
                                "com"
                            ],
                            "path": [
                                "v1",
                                "deliveries",
                                "groups",
                                "0",
                                "{trigger_timestamp}",
                                "trigger"
                            ]
                        }
                    },
                    "response": []
                }
            '''
            item = item.replace("{trigger_algo_wait_miliseconds}",
                         str(trigger_algo_wait_miliseconds))
            item = item.replace("{new_api_subdomain}", new_api_subdomains[env])
            item = item.replace("{trigger_timestamp}", trigger_timearg)
            requests.append(item)

        items = ",".join(requests)
        ostream.write('''
{
    "info": {
        "_postman_id": "375540f6-b06d-4bc1-9ef0-ba48521d0791",
        "name": "post-300",
        "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"
    },
    "item": [''')
        ostream.write(items)
        #ostream.write(json.dumps(items))
        ostream.write('''
    ],''')
        event_body = '''
    "event": [
        {
            "listen": "prerequest",
            "script": {
                "id": "3cb62e39-c23f-47e5-a15f-7696126491c8",
                "type": "text/javascript",
                "exec": [{pr_scripts}]            
            }
        },
        {
            "listen": "test",
            "script": {
                "id": "0ae33bcf-3dcc-433d-bcb1-f31ef1ae1d12",
                "type": "text/javascript",
                "exec": [{te_scripts}]
            }
        }
    ],
        '''
        p_events = '"' + '","'.join(pr_events) + '"'
        t_scripts = '"' + '","'.join(te_events) + '"'
        event_body = event_body.replace('{pr_scripts}', p_events)
        event_body = event_body.replace('{te_scripts}', t_scripts)

        ostream.write(event_body)
        ostream.write('''
    \n\t\"protocolProfileBehaviour\": \"\"
}\n''')
