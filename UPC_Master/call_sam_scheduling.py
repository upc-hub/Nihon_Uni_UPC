import requests
import json
import os
import codecs

def auto_generate(typea, typeb, typec, typed, typee, typef):
  url = "http://localhost:9000/aplas/scheduling"

  payload = json.dumps({
    "params": [
      {
        "job_type": "BassixAppX1",
        "job_amount": typea
      },
      {
        "job_type": "BassixAppX2",
        "job_amount": typeb
      },
      {
        "job_type": "ColorGame",
        "job_amount": typec
      },
      {
        "job_type": "SoccerMatch",
        "job_amount": typed
      },
      {
        "job_type": "AnimalTour",
        "job_amount": typee
      },
      {
        "job_type": "MyLibrary",
        "job_amount": typef
      }
    ]
  })
  headers = {
    'Content-Type': 'application/json'
  }

  response = requests.request("POST", url, headers=headers, data=payload)
  json_data = json.loads(response.text)
  with codecs.open('./data.json', 'w', 'utf8') as f:
    f.write(json.dumps(json_data, sort_keys = True, ensure_ascii=False))

if __name__ == "__main__":
  import argparse
  parser = argparse.ArgumentParser(description="Sam san shceduling")
  parser.add_argument("type1", help="number of type-1 jobs")
  parser.add_argument("type2", help="number of type-2 jobs")
  parser.add_argument("type3", help="number of type-3 jobs")
  parser.add_argument("type4", help="number of type-4 jobs")
  parser.add_argument("type5", help="number of type-5 jobs")
  parser.add_argument("type6", help="number of type-6 jobs")
  args = parser.parse_args()
  typea = args.type1
  typeb = args.type2
  typec = args.type3
  typed = args.type4
  typee = args.type5
  typef = args.type6
  auto_generate(typea, typeb, typec, typed, typee, typef)