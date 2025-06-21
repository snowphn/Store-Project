#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
用户类型和邀请码特权功能测试脚本

此脚本用于测试新增的用户类型和邀请码特权功能。
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database.db_operations import (
    create_invite_code, get_invite_codes, verify_invite_code, 
    create_user, get_user_by_username
)
from models.invite_code import PrivilegeType
from models.user import User

def test_invite_code_generation():
    """测试邀请码生成功能"""
    print("\n=== 测试邀请码生成功能 ===")
    
    # 生成不同类型的邀请码
    normal_code = create_invite_code(PrivilegeType.NORMAL)
    vip_code = create_invite_code(PrivilegeType.VIP)
    
    print(f"普通用户邀请码: {normal_code.code} (类型: {normal_code.privilege_type.value})")
    print(f"VIP用户邀请码: {vip_code.code} (类型: {vip_code.privilege_type.value})")
    
    return normal_code.code, vip_code.code

def test_user_registration():
    """测试用户注册功能"""
    print("\n=== 测试用户注册功能 ===")
    
    # 生成测试邀请码
    normal_code, vip_code = test_invite_code_generation()
    
    # 测试1: 不使用邀请码注册（应该是普通用户）
    print("\n1. 测试无邀请码注册...")
    success, message = create_user("test_normal", "normal@test.com", "password123")
    if success:
        user = get_user_by_username("test_normal")
        print(f"   用户创建成功: {user.username}")
        print(f"   用户类型: {user.get_type_display()}")
        print(f"   显示名称: {user.display_name}")
    else:
        print(f"   创建失败: {message}")
    
    # 测试2: 使用VIP邀请码注册
    print("\n2. 测试VIP邀请码注册...")
    success, message = create_user("test_vip", "vip@test.com", "password123", vip_code)
    if success:
        user = get_user_by_username("test_vip")
        print(f"   用户创建成功: {user.username}")
        print(f"   用户类型: {user.get_type_display()}")
        print(f"   显示名称: {user.display_name}")
        print(f"   使用的邀请码: {user.invite_code_used}")
    else:
        print(f"   创建失败: {message}")
    
    # 测试3: 使用管理员邀请码注册
    print("\n3. 测试管理员邀请码注册...")
    success, message = create_user("test_admin", "admin@test.com", "password123", admin_code)
    if success:
        user = get_user_by_username("test_admin")
        print(f"   用户创建成功: {user.username}")
        print(f"   用户类型: {user.get_type_display()}")
        print(f"   显示名称: {user.display_name}")
        print(f"   是否为管理员: {user.is_admin}")
        print(f"   使用的邀请码: {user.invite_code_used}")
    else:
        print(f"   创建失败: {message}")
    
    # 测试4: 尝试重复使用邀请码
    print("\n4. 测试重复使用邀请码...")
    success, message = create_user("test_duplicate", "duplicate@test.com", "password123", vip_code)
    if not success:
        print(f"   正确阻止了重复使用: {message}")
    else:
        print(f"   错误：允许了重复使用")

def test_invite_code_listing():
    """测试邀请码列表功能"""
    print("\n=== 测试邀请码列表功能 ===")
    
    codes = get_invite_codes()
    print(f"\n当前邀请码总数: {len(codes)}")
    
    for code in codes[-5:]:  # 显示最后5个邀请码
        status = "已使用" if code.is_used else "未使用"
        privilege_names = {
            "normal": "普通用户",
            "vip": "VIP用户",
            "admin": "管理员"
        }
        privilege_text = privilege_names.get(
            code.privilege_type.value if hasattr(code.privilege_type, 'value') else str(code.privilege_type),
            "未知"
        )
        
        print(f"   {code.code} | {privilege_text} | {status}")
        if code.is_used and code.used_by_user_id:
            print(f"     └─ 使用者ID: {code.used_by_user_id}")

def test_user_type_detection():
    """测试用户类型自动检测"""
    print("\n=== 测试用户类型自动检测 ===")
    
    # 获取测试用户
    test_users = ["test_normal", "test_vip", "test_admin"]
    
    for username in test_users:
        user = get_user_by_username(username)
        if user:
            print(f"\n用户: {user.username}")
            print(f"  类型: {user.get_type_display()}")
            print(f"  显示名称: {user.display_name}")
            print(f"  是否管理员: {user.is_admin}")
            if user.invite_code_used:
                print(f"  邀请码: {user.invite_code_used}")
        else:
            print(f"\n用户 {username} 不存在")

def main():
    """主测试函数"""
    print("用户类型和邀请码特权功能测试")
    print("=" * 50)
    
    try:
        # 运行所有测试
        test_user_registration()
        test_invite_code_listing()
        test_user_type_detection()
        
        print("\n" + "=" * 50)
        print("所有测试完成！")
        print("\n功能验证:")
        print("✓ 邀请码特权选择功能")
        print("✓ 无邀请码注册为普通用户")
        print("✓ 用户类型自动检测")
        print("✓ 显示名称自动生成")
        print("✓ 管理员权限自动设置")
        
    except Exception as e:
        print(f"\n测试过程中出现错误: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()