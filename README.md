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
  ```
- **数据集说明**：
  - 缺省使用 `test.json` 中的数据（1000条记录）进行评测。
  - 数据集需符合 alpaca 格式的 json 文件，可以作为 `--dateset` 参数指定。

# 3. 参与贡献
- **开发模型**：本程序主要使用 deepseek code 模型编写。
