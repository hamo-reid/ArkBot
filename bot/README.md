# ArkBot

## How to start

1. generate project using `nb create` .
2. create your plugin using `nb plugin create` .
3. writing your plugins under `src/plugins` folder.
4. run your bot using `nb run` .

## Documentation

See [Docs](https://v2.nonebot.dev/)

## 项目结构

顶级的结构
bot: 机器人后端（Nonebot框架）
gocq: 无头QQ（负责和腾讯交互）

1. bot -> gocq发信息 -> 腾讯
2. 腾讯 -> gocq接收 -> bot处理

## bot 插件结构

- Core: 他和nonebot无关，他负责游戏数据的更新、检索、处理、图片生成（可能分离）
- 