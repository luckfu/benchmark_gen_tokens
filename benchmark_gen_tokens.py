import requests
import time
import json
import argparse
import csv
from tqdm import tqdm
from multiprocessing import Pool, cpu_count

# 定义一个全局函数来处理单个消息
def process_message(api_key, url, model, max_tokens, message):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    data = {
        "model": model,
        "messages": [{"role": "user", "content": message["content"]}],
        "max_tokens": max_tokens
    }

    start_time = time.time()
    response = requests.post(url, headers=headers, data=json.dumps(data))
    end_time = time.time()

    generation_time = end_time - start_time
    response_json = response.json()
    generated_tokens = response_json['usage']['completion_tokens']  # 使用API响应中的usage字段
    answer = response_json['choices'][0]['message']['content']

    return generation_time, generated_tokens, message["content"], answer

# 定义一个函数来测量生成tokens的时间
def measure_generation_speed(api_key, url, model, messages, max_tokens, n, process_id):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    total_time = 0
    total_tokens = 0
    total_steps = n * len(messages)  # 计算总步数

    # 打开CSV文件进行写入
    with open(f'test_out_process_{process_id}.csv', 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['question', 'answer']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        progress_bar = tqdm(total=total_steps, desc=f"Processing (Process {process_id})")

        for _ in range(n):
            for message in messages:
                generation_time, generated_tokens, question, answer = process_message(api_key, url, model, max_tokens, message)
                total_time += generation_time
                total_tokens += generated_tokens

                # 写入CSV文件
                writer.writerow({'question': question, 'answer': answer})

                # 更新进度条
                progress_bar.update(1)

        progress_bar.close()

    average_time = total_time / total_steps
    average_tokens = total_tokens / total_steps
    tokens_per_second = average_tokens / average_time

    print(f"Process {process_id} - Average generation time: {average_time:.2f} seconds")
    print(f"Process {process_id} - Tokens per second: {tokens_per_second:.2f}")
    print(f"Process {process_id} - Total tokens generated: {total_tokens}")

    return total_time, total_tokens

# 解析命令行参数
def main():
    parser = argparse.ArgumentParser(description="Measure API generation speed.")
    parser.add_argument("--url", required=True, help="API URL, Sample:https://api.openai.com/v1/chat/completions")
    parser.add_argument("--api_key", default="", help="API key (optional)")
    parser.add_argument("--model", required=True, help="Model name Sample: gpt-3.5-turbo")
    parser.add_argument("--max_tokens", type=int, default=2048, help="Maximum tokens to generate")
    parser.add_argument("--n", type=int, default=1, help="Number of runs")
    parser.add_argument("--dataset", default="test.json", help="Path to the JSON dataset file")
    parser.add_argument("--processes", type=int, default=cpu_count(), help="Number of concurrent processes")
    args = parser.parse_args()

    with open(args.dataset, 'r', encoding='utf-8') as file:
        dataset = json.load(file)

    messages = [
        {"role": "user", "content": item["instruction"] + " " + item["input"]}
        for item in dataset
    ]

    with Pool(processes=args.processes) as pool:
        results = [pool.apply_async(measure_generation_speed, (args.api_key, args.url, args.model, messages, args.max_tokens, args.n, i)) for i in range(args.processes)]

        total_time = 0
        total_tokens = 0

        for result in results:
            process_total_time, process_total_tokens = result.get()
            total_time += process_total_time
            total_tokens += process_total_tokens

        total_steps = args.n * len(messages) * args.processes
        average_time = total_time / total_steps
        average_tokens = total_tokens / total_steps
        tokens_per_second = average_tokens / average_time

        print(f"Overall - Average generation time: {average_time:.2f} seconds")
        print(f"Overall - Tokens per second: {tokens_per_second:.2f}")
        print(f"Overall - Total tokens generated: {total_tokens}")

if __name__ == "__main__":
    main()