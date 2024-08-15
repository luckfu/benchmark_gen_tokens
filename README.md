# 1. 介绍
- **目的**：测试在私有环境中部署的兼容OpenAI API模式的LLM（大型语言模型）服务中，生成tokens的速度。

# 2. 使用说明
- **查看执行参数**：
  ```bash
  python benchmark_gen_tokens.py --help
  ```
- **执行命令示例**：
  ```bash
  python benchmark_gen_tokens.py --url https://api.openai.com/v1/chat/completions --api_key [key] --model [model name] --max_tokens 512 --n 1 --process 2 --dateset [test.json]

  Processing (Process 0): 100%|████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 10/10 [01:33<00:00,  9.32s/it]
  Process 0 - Average generation time: 9.32 seconds
  Process 0 - Tokens per second: 17.09
  Process 0 - Total tokens generated: 1593
  Processing (Process 1): 100%|████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 10/10 [01:57<00:00, 11.79s/it]
  Process 1 - Average generation time: 11.79 seconds
  Process 1 - Tokens per second: 17.92
  Process 1 - Total tokens generated: 2113
  Overall - Average generation time: 10.56 seconds
  Overall - Tokens per second: 17.55
  Overall - Total tokens generated: 3706
  ```
- **数据集说明**：
  - 缺省使用 `test.json` 中的数据（1000条记录）进行评测。
  - 数据集需符合 alpaca 格式的 json 文件，可以作为 `--dateset` 参数指定。

# 3. 参与贡献
- **开发模型**：本程序主要使用 deepseek code 模型编写。
