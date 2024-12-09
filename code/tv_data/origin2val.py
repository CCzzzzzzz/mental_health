# -*- coding: utf-8 -*-
import json

# 读取JSON文件
with open('../../data/train_re.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

# 遍历每个数据项，修改 instruction 中的内容
# for item in data:
#     output_entities = set(item['output'].split(';'))  # 使用集合去除重复的实体类型
#     output_entities = [entity.split(':')[0] for entity in output_entities]  # 提取实体类型
#     output_entities = list(set(output_entities))  # 去除重复的实体类型
#     # instruction = "作为一名出色的心理学专家，您的任务是分析以下句子中的所有实体类型，包括性别、年龄、职业、躯体状况、情绪状况、家庭结构和想法，其中，情绪状况为情绪或心理，如伤心、焦虑等，躯体状况为各种生理反应，如失眠，呕吐，家庭结构指家里或家族里的成员，想法指个体在遇到诱发性事件后产生的信念。请确认是否每个句子都包含有关{}的信息。如果句子都包含这些信息，请回答正确；否则，请回答错误。句子为：".format('、'.join(output_entities), '、'.join(output_entities))
#     # instruction = "作为一名出色的心理学专家，您的任务是分析以下句子中的所有事件类型，包括引发事件和过去经历，其中，引发事件指的是文本中出现的引发当前情绪或躯体状况的导火索事件，过去经历指的是文本中过去发生的事情。请确认是否每个句子都包含有关{}的信息。如果句子都包含这些信息，请回答正确；否则，请回答错误。句子为：".format('、'.join(output_entities), '、'.join(output_entities))
#     instruction = "分析句子中的所有实体类型，包括性别、年龄、职业、躯体状况、情绪状况、家庭结构和想法，其中，情绪状况为情绪或心理，如伤心、焦虑等，躯体状况为各种生理反应，如失眠，呕吐，家庭结构指家里或家族里的成员，想法指个体在遇到诱发性事件后产生的信念。请确认是否每个句子都包含有关{}的实体类型。如果句子都包含这些实体类型或不缺失其他实体类型，请回答正确；否则，请回答错误。句子为：".format('、'.join(output_entities), '、'.join(output_entities))
#     # instruction = "分析句子中的所有事件类型，包括引发事件和过去经历，其中，引发事件指的是文本中出现的引发当前情绪或躯体状况的导火索事件，过去经历指的是文本中过去发生的事情。请确认是否每个句子都包含有关{}的事件类型。如果句子都包含这些事件类型或不缺失其他事件类型，请回答正确；否则，请回答错误。句子为：".format('、'.join(output_entities), '、'.join(output_entities))
#
#     # instruction = "作为一名出色的心理学专家，您的任务是分析以下句子中的所有实体类型。请确认是否每个句子都包含有关{}的实体类型。如果句子都包含这些实体类型，请回答正确；否则，请回答错误。句子为：".format('、'.join(output_entities), '、'.join(output_entities))
#     # instruction = "作为一名出色的心理学专家，您的任务是分析以下句子中的所有事件类型。请确认是否每个句子都包含有关{}的事件类型。如果句子都包含这些事件类型，请回答正确；否则，请回答错误。句子为：".format('、'.join(output_entities), '、'.join(output_entities))
#     item['instruction'] = instruction
#     item['output'] = "正确"

for item in data:
    output_entities = item['output'].split(';')
    unique_entities = set()
    for entity in output_entities:
        parts = entity.split(':')
        if len(parts) == 3:  # 处理特殊格式的情况
            unique_entities.add(parts[1])
        else:
            unique_entities.add(parts[0])

    instruction = "分析句子中的所有关系类型，包括家庭亲近、家庭疏远、同伴亲近、同伴疏远、源自和产生，其中，源自的主体为主观想法(表示个体对这个事件的一些信念)。客体为事件，产生的主体为事件，客体为情绪(如焦虑，生气等)。请确认是否每个句子都包含有关{}的关系类型。如果句子都包含这些关系类型或不缺失其他关系类型，请回答正确；否则，请回答错误。句子为：".format('、'.join(unique_entities), '、'.join(unique_entities))
    item['instruction'] = instruction
    item['output'] = "正确"

# 写回新的JSON文件
with open('./val_data/val_re1.json', 'w', encoding='utf-8') as file:
    json.dump(data, file, ensure_ascii=False, indent=4)
