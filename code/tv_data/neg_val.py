# import json
# import random
#
# # 读取原始JSON数据
# with open('./val_data/test_ner1.json', 'r', encoding='utf-8') as f:
#     data = json.load(f)
#
# for sample in data:
#     # 选择一个与当前样本instruction不同的样本
#     different_samples = [s for s in data if s['instruction'] != sample['instruction']]
#     different_sample = random.choice(different_samples)
#
#     # 替换input字段为选择的不同样本的input内容
#     sample['input'] = different_sample['input']
#
#     # 修改output字段为"错误"
#     sample['output'] = "错误"
#
# # 将修改后的数据写入新的JSON文件
# with open('./val_data/test_ner2.json', 'w', encoding='utf-8') as f:
#     json.dump(data, f, ensure_ascii=False, indent=4)

import json
import random

def create_negative_samples(input_file, output_file, num_negative_samples):
    # 读取原始JSON数据
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    modified_data = []
    for sample in data:
        # 选择num_negative_samples个与当前样本instruction不同的样本
        different_samples = [s for s in data if s['instruction'] != sample['instruction']]
        different_samples = random.sample(different_samples, num_negative_samples)

        for different_sample in different_samples:
            modified_sample = {
                'instruction': sample['instruction'],
                'input': different_sample['input'],
                'output': "错误"
            }
            modified_data.append(modified_sample)

    # 将修改后的数据写入新的JSON文件
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(modified_data, f, ensure_ascii=False, indent=4)

# 调用函数并指定负样本数量
create_negative_samples('./val_data/test_ee1.json', './val_data/test_ee3.json', num_negative_samples=2)
