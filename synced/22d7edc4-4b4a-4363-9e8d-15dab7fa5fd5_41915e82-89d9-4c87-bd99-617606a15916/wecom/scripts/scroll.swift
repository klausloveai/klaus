// 在屏幕坐标 (x, y)（单位：point）处发送滚轮事件。用法：scroll x y lines（正数往上滚）
import CoreGraphics
import Foundation
let a = CommandLine.arguments
let x = Double(a[1])!, y = Double(a[2])!, lines = Int32(a[3])!
let p = CGPoint(x: x, y: y)
CGEvent(mouseEventSource: nil, mouseType: .mouseMoved, mouseCursorPosition: p, mouseButton: .left)?.post(tap: .cghidEventTap)
usleep(50_000)
let e = CGEvent(scrollWheelEvent2Source: nil, units: .line, wheelCount: 1, wheel1: lines, wheel2: 0, wheel3: 0)!
e.location = p
e.post(tap: .cghidEventTap)
