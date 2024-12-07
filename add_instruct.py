import json

def add_predict_and_result(first_file_path, second_file_path, output_file_path):
    # 读取第一个JSON文件
    with open(first_file_path, 'r', encoding='utf-8') as f:
        first_data = json.load(f)

    # 读取第二个JSON文件
    with open(second_file_path, 'r', encoding='utf-8') as f:
        second_data = json.load(f)

    # 获取第一个文件的前202条记录
    if 'test_ner' in second_file_path:
        first_data_subset = first_data[:202]
    elif 'test_re' in second_file_path:
        first_data_subset = first_data[202:404]
    elif 'test_ee' in second_file_path:
        first_data_subset = first_data[-201:]

    # 将predict和result字段添加到第二个文件的相应记录中
    for i, record in enumerate(second_data):
        if i < len(first_data_subset):
            record['predict'] = first_data_subset[i]['predict']
            record['result'] = first_data_subset[i]['result']
            record['type_predict'] = first_data_subset[i]['type_predict']

            if record['type_predict'] == '错误' and 'test_ner' in second_file_path:
                record['system'] = ''
                record['system'] += '实体类型包含{}的回答是错的。请重新回答'.format(
                    '、'.join(set([entity.split(':')[0] for entity in record['predict'].split(';')])))

            if record['type_predict'] == '错误' and 'test_re' in second_file_path:
                record['system'] = ''
                record['system'] += '回答时注意关系类型包含{}的答案是错的。请重新回答'.format(
                    '、'.join(set([entity.split(':')[1] for entity in record['predict'].split(';')])))

            if record['type_predict'] == '错误' and 'test_ee' in second_file_path:
                record['system'] = ''
                record['system'] += '事件类型包含{}的回答是错的。请重新回答'.format(
                '、'.join(set([entity.split(':')[0] for entity in record['predict'].split(';')])))

    # 将更新后的数据写入新的JSON文件
    with open(output_file_path, 'w', encoding='utf-8') as f:
        json.dump(second_data, f, ensure_ascii=False, indent=4)

def add_type_predict_field(json_file, json_file1, json_file2, json_file3, jsonl_file, output_file):
    # 读取第一个JSON文件
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # 读取第二个JSON文件
    with open(json_file1, 'r', encoding='utf-8') as f:
        data1 = json.load(f)

    # 读取第三个JSON文件
    with open(json_file2, 'r', encoding='utf-8') as f:
        data2 = json.load(f)

    # 读取第四个JSON文件
    with open(json_file3, 'r', encoding='utf-8') as f:
        data3 = json.load(f)

    # 读取JSONL文件，提取predict字段
    with open(jsonl_file, 'r', encoding='utf-8') as f:
        predict_data = [json.loads(line)['predict'] for line in f]

    # 将predict字段赋值给type_predict字段
    for i, record in enumerate(data):
        if i < len(predict_data):
            record['type_predict'] = predict_data[i]

    # 将json_file1中的instruction字段赋值给json_file中的前202条记录的instruction字段
    for i, record in enumerate(data):
        if i < 202 and i < len(data1):
            record['instruction'] = data1[i]['instruction']

    # 将json_file2中的instruction字段赋值给json_file中的第203到404条记录的instruction字段
    for i, record in enumerate(data):
        if 202 <= i < 404 and i-202 < len(data2):
            record['instruction'] = data2[i-202]['instruction']

    # 将json_file3中的instruction字段赋值给json_file中的后201条记录的instruction字段
    for i, record in enumerate(data[403:], start=403):
        if i-403 < len(data3):
            record['instruction'] = data3[i-403]['instruction']

    # 写入修改后的数据到新的JSON文件
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


add_type_predict_field('../model_result/other_model/llama3_val_test.json', '../model_result/test_ner.json',  '../model_result/test_re.json', '../model_result/test_ee.json', 'predictions.jsonl', './llama3/val_predict.json')

add_predict_and_result('./llama3/val_predict.json', '../model_result/test_ner.json', './llama3/revise_ner.json')
add_predict_and_result('./llama3/val_predict.json', '../model_result/test_re.json', './llama3/revise_re.json')
add_predict_and_result('./llama3/val_predict.json', '../model_result/test_ee.json', './llama3/revise_ee.json')
