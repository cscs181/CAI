<p align="center">
  <a href="#"><img src="https://raw.githubusercontent.com/cscs181/CAI/master/docs/assets/logo_text.png" width="40%" alt="CAI"></a>
</p>

<div align="center">

_✨ Yet Another Bot Framework for Tencent QQ Written in Python ✨_

</div>

<p align="center">
  <a href="https://github.com/cscs181/CAI/blob/master/LICENSE">
    <img src="https://img.shields.io/github/license/cscs181/CAI" alt="license">
  </a>
  <img src="https://img.shields.io/badge/python-3.7+-blue" alt="python">
  <a target="_blank" href="https://github.com/sindresorhus/awesome">
    <img src="https://cdn.rawgit.com/sindresorhus/awesome/d7305f38d29fed78fa85652e3a63e154dd8e8829/media/badge.svg">
  </a>
  <a target="_blank" href="https://qm.qq.com/cgi-bin/qm/qr?k=1SsvybRcQrgt6Kd5fV9W2Kpfje0l3VFw&jump_from=webapi">
    <img src="https://img.shields.io/badge/qq%E7%BE%A4-552362998-success" alt="QQ Chat">
  </a>
</p>

---

## 声明

### 一切开发旨在学习，请勿用于非法用途

- `CAI` 是完全免费且开放源代码的软件，仅供学习和娱乐用途使用
- `CAI` 不会通过任何方式强制收取费用，或对使用者提出物质条件

### 许可证

`CAI` 采用 [AGPLv3](LICENSE) 协议开源，不鼓励、不支持一切商业使用。

---

## 特色

- 简单易用的 API，支持多账号
- 极少的额外依赖
- 异步编写，效率++

  - 使用 [Asyncio Stream](https://docs.python.org/3/library/asyncio-stream.html) 处理网络连接 ([cai.connection.Connection](https://cai-bot.readthedocs.io/zh_CN/latest/source/cai.connection.html#cai.connection.Connection))
  - 使用 [Asyncio Future](https://docs.python.org/3/library/asyncio-future.html) 处理收发包 ([cai.utils.future.FutureStore](https://cai-bot.readthedocs.io/zh_CN/latest/source/cai.utils.html#cai.utils.future.FutureStore))

- 完整的 [Type Hints](https://www.python.org/dev/peps/pep-0484/)

  - Packet Query 支持 [Variadic Generics](https://www.python.org/dev/peps/pep-0646/)

    ```python
    from cai.utils.binary import Packet
    packet = Packet(bytes.fromhex("01000233000000"))
    packet.start().int8().uint16().bytes(4).execute()
    # return type: INT8, UINT16, BYTES
    ```

  - 便携的 JceStruct 定义 (使用方法参考 [JceStruct](https://github.com/yanyongyu/JceStruct))

    ```python
    from typing import Optional
    from jce import JceStruct, JceField, types

    class CustomStruct(JceStruct):
        int32_field: types.INT32 = JceField(jce_id=0)
        optional_field: Optional[types.DOUBLE] = JceField(None, jce_id=1)
        nested_field: OtherStruct = JceField(jce_id=2)
    ```

## 功能

`CAI` 仅作为底层协议库使用，将协议封装为 API。

> `CAI` 不会支持涉及 **金钱**、**主动邀请**、**获取凭证** 等敏感操作的协议。

<details>
<summary>已支持的协议列表：</summary>

### 登录

[`cai.api.login` API Reference](https://cai-bot.readthedocs.io/zh_CN/latest/source/cai.api.html#module-cai.api.login)

- [x] 账号密码登录
- [x] 设备锁验证
- [x] 图片验证码提交
- [x] 短信验证码提交
- [ ] 扫码登录

### 客户端

[`cai.api.client` API Reference](https://cai-bot.readthedocs.io/zh_CN/latest/source/cai.api.html#module-cai.api.client)

- [x] 设置在线状态

### 好友

[`cai.api.friend` API Reference](https://cai-bot.readthedocs.io/zh_CN/latest/source/cai.api.html#module-cai.api.friend)

- [x] 获取好友列表
- [x] 获取好友信息
- [x] 获取好友分组列表
- [x] 获取好友分组信息

### 群组

[`cai.api.group` API Reference](https://cai-bot.readthedocs.io/zh_CN/latest/source/cai.api.html#module-cai.api.group)

- [x] 获取群列表
- [x] 获取群信息
- [x] 获取群成员列表

### 事件

[`cai.api.flow` API Reference](https://cai-bot.readthedocs.io/zh_CN/latest/source/cai.api.html#module-cai.api.flow)

通过注册事件监听回调，在事件发生时执行指定操作。事件类型可通过 `cai.client` 模块导入。

- [x] 好友消息 ([PrivateMessage](https://cai-bot.readthedocs.io/zh_CN/latest/source/cai.client.message_service.html#cai.client.message_service.models.PrivateMessage))
- [x] 群消息 ([GroupMessage](https://cai-bot.readthedocs.io/zh_CN/latest/source/cai.client.message_service.html#cai.client.message_service.models.GroupMessage))

</details>

## 文档

_In Development_

[See on Read The Docs](https://cai-bot.readthedocs.io/)
