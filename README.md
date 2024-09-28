

Ask for code repo

```
python llm.py --context /tmp/repo.git --chat --sys_prompt repo
```

在代码库中根据关键词出现的上下文询问问题 (省 token)

```
rg -N  onnx magika-main --type py --type rust  -B 5 | python llm.py --pipe --prompt "oonx 是如何被加载的"
```



Ask for url

```
python llm.py --url https://blog.torproject.org/tor-is-still-safe --chat 
```

Ask for youtube

```
python llm.py --youtube https://www.youtube.com/watch?v=R8uxmXmtOrk --chat
[...]
> .md
Switching to markdown mode
> 总结
这段对话是 George Hotz 关于他的编程工作，特别是 Tinygrad 的更新和快速蒙特卡洛树搜索 (MCTS) 的直播。
他重点介绍了 Tinygrad 的几个新特性：
 • 更精确的初始化： Tinygrad 的初始化现在更简单，导致模型精度更高。    
 • AMD GPU 支持： Tinygrad 现在支持 AMD 和 Nvidia GPU，这扩展了其适用性。
[...]
```
