import json


with open("../out/result_depth1_mq1_zeroshot_gpt-4o-mini0.json", "r") as json_file :
    data = json.load(json_file)

avg_ftime = 0
avg_btime = 0
avg_ctime = 0


for d in data :
    avg_ftime += d["forward_time"]
    avg_btime += d["backward_time"]
    avg_ctime += d["cot_fewshot_time"]

avg_ftime /= len(data)
avg_btime /= len(data)
avg_ctime /= len(data)

print(f"""[Average inference time]
      forward : {round(avg_ftime,2)} sec
      backward : {round(avg_btime, 2)} sec
      cot : {round(avg_ctime, 2)} sec
      total : {round(avg_ftime+avg_btime, 2)} sec
      """)