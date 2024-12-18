from flask import Flask, render_template, request, jsonify
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
from peft import PeftModel
import os
import json
from collections import OrderedDict
from flask import Response
app = Flask(__name__)
# app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
# 模型路径配置
mode_path = "/root/autodl-tmp/LLM-Research/Meta-Llama-3___1-8B-Instruct"
lora_path = "output/llama3_1_instruct_lora/checkpoint-165"

# 初始化模型和 tokenizer
tokenizer = AutoTokenizer.from_pretrained(mode_path, trust_remote_code=True)
model = AutoModelForCausalLM.from_pretrained(
    mode_path, device_map="auto", torch_dtype=torch.bfloat16, trust_remote_code=True
).eval()
model = PeftModel.from_pretrained(model, model_id=lora_path)

# 读取物品分类数据
with open("dataset/item_list.json", "r", encoding="utf-8") as f:
    item_data = json.load(f)

# 按分类分组数据
grouped_data = {}
for item in item_data:
    category = item["分类"]
    if category not in grouped_data:
        grouped_data[category] = []
    grouped_data[category].append(item["物品名称"])
sorted_grouped_data = OrderedDict(sorted(grouped_data.items(), key=lambda x: len(x[1]), reverse=True))
# print(sorted_grouped_data)
@app.route("/test_items", methods=["GET"])
def test_items():
    """测试分组后的 JSON 数据"""
    json_data = json.dumps(sorted_grouped_data, ensure_ascii=False, indent=2, sort_keys=False)
    return Response(json_data, mimetype="application/json")
@app.route("/get_items", methods=["GET"])
def get_items():
    """返回分组后的物品分类数据"""
    json_data = json.dumps(sorted_grouped_data, ensure_ascii=False, indent=2, sort_keys=False)
    return Response(json_data, mimetype="application/json")
@app.route("/")
def index():
    """渲染主页并传递分组数据"""
    return render_template("index.html")  
@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_input = data.get("message", "").strip()

    if not user_input:
        return jsonify({"error": "输入内容不能为空！"}), 400

    # 构建对话输入
    messages = [
        {"role": "system", "content": "假设你是Minecraft的NPC。"},
        {"role": "user", "content": user_input},
    ]
    input_ids = tokenizer.apply_chat_template(
        messages, tokenize=False, add_generation_prompt=True
    )

    model_inputs = tokenizer([input_ids], return_tensors="pt").to("cuda")  # 确保输入数据在 CUDA 上

    # 模型生成
    generated_ids = model.generate(model_inputs.input_ids, max_new_tokens=512)

    # 解析生成结果
    generated_ids = [
        output_ids[len(model_inputs.input_ids[0]):]
        for output_ids in generated_ids
    ]
    response = tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0]

    return jsonify({"response": response})

if __name__ == "__main__":
    app.run(debug=True,host="0.0.0.0",port=6666)

