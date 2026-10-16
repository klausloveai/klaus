// 等价于技能自带的 scroll.swift，因 CLT 的 swiftc 比系统 SDK 旧编不过，改用 clang 编译。
// 在屏幕坐标 (x, y)（单位：point）处发送滚轮事件。用法：scroll x y lines（正数往上滚）
#include <ApplicationServices/ApplicationServices.h>
#include <stdlib.h>
#include <unistd.h>

int main(int argc, char **argv) {
  if (argc < 4) return 2;
  CGPoint p = CGPointMake(atof(argv[1]), atof(argv[2]));
  int32_t lines = (int32_t)atoi(argv[3]);

  CGEventRef move = CGEventCreateMouseEvent(NULL, kCGEventMouseMoved, p, kCGMouseButtonLeft);
  if (move) { CGEventPost(kCGHIDEventTap, move); CFRelease(move); }
  usleep(50000);

  CGEventRef ev = CGEventCreateScrollWheelEvent2(NULL, kCGScrollEventUnitLine, 1, lines, 0, 0);
  if (!ev) return 1;
  CGEventSetLocation(ev, p);
  CGEventPost(kCGHIDEventTap, ev);
  CFRelease(ev);
  return 0;
}
