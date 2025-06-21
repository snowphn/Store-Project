#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数据库迁移脚本：添加用户类型和邀请码特权功能

此脚本用于将现有数据库升级到支持用户类型和邀请码特权的新版本。
运行此脚本前请备份数据库！
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import text
from database.db_init import SessionLocal, engine
from models.user import User
from models.invite_code import InviteCode, PrivilegeType

def migrate_database():
    """执行数据库迁移"""
    print("开始数据库迁移...")
    
    db = SessionLocal()
    try:
        # 1. 为invite_codes表添加新字段
        print("1. 更新邀请码表结构...")
        try:
            # 添加privilege_type字段
            db.execute(text("""
                ALTER TABLE invite_codes 
                ADD COLUMN privilege_type VARCHAR(20) DEFAULT 'normal' NOT NULL
            """))
            print("   - 添加privilege_type字段")
        except Exception as e:
            if "already exists" not in str(e).lower():
                print(f"   - 警告: {e}")
        
        try:
            # 添加used_by_user_id字段
            db.execute(text("""
                ALTER TABLE invite_codes 
                ADD COLUMN used_by_user_id INTEGER
            """))
            print("   - 添加used_by_user_id字段")
        except Exception as e:
            if "already exists" not in str(e).lower():
                print(f"   - 警告: {e}")
        
        # 2. 为users表添加新字段
        print("2. 更新用户表结构...")
        try:
            # 添加user_type字段
            db.execute(text("""
                ALTER TABLE users 
                ADD COLUMN user_type VARCHAR(20) DEFAULT 'normal' NOT NULL
            """))
            print("   - 添加user_type字段")
        except Exception as e:
            if "already exists" not in str(e).lower():
                print(f"   - 警告: {e}")
        
        try:
            # 添加display_name字段
            db.execute(text("""
                ALTER TABLE users 
                ADD COLUMN display_name VARCHAR(100)
            """))
            print("   - 添加display_name字段")
        except Exception as e:
            if "already exists" not in str(e).lower():
                print(f"   - 警告: {e}")
        
        try:
            # 添加invite_code_used字段
            db.execute(text("""
                ALTER TABLE users 
                ADD COLUMN invite_code_used VARCHAR(20)
            """))
            print("   - 添加invite_code_used字段")
        except Exception as e:
            if "already exists" not in str(e).lower():
                print(f"   - 警告: {e}")
        
        db.commit()
        
        # 3. 更新现有数据
        print("3. 更新现有数据...")
        
        # 为现有管理员用户设置admin类型
        admin_users = db.query(User).filter(User.is_admin == True).all()
        for user in admin_users:
            user.user_type = PrivilegeType.ADMIN
            if not user.display_name:
                user.display_name = f"管理员 - {user.username}"
        print(f"   - 更新了 {len(admin_users)} 个管理员用户")
        
        # 为现有普通用户设置normal类型和显示名称
        normal_users = db.query(User).filter(User.is_admin == False).all()
        for user in normal_users:
            user.user_type = PrivilegeType.NORMAL
            if not user.display_name:
                user.display_name = f"普通用户 - {user.username}"
        print(f"   - 更新了 {len(normal_users)} 个普通用户")
        
        db.commit()
        
        print("\n数据库迁移完成！")
        print("\n新功能说明:")
        print("- 邀请码现在支持特权选择（普通用户、VIP用户、管理员）")
        print("- 用户注册时如果不填邀请码将自动成为普通用户")
        print("- 系统会自动为用户生成显示名称，格式为：用户类型 - 用户名")
        print("- 管理员界面现在显示用户类型和使用的邀请码信息")
        
    except Exception as e:
        db.rollback()
        print(f"迁移失败: {e}")
        raise
    finally:
        db.close()

def check_migration_needed():
    """检查是否需要迁移"""
    db = SessionLocal()
    try:
        # 检查是否已经有新字段
        result = db.execute(text("""
            SELECT COUNT(*) as count
            FROM pragma_table_info('users') 
            WHERE name = 'user_type'
        """))
        
        has_user_type = result.fetchone()[0] > 0
        
        if has_user_type:
            print("数据库已经是最新版本，无需迁移。")
            return False
        else:
            print("检测到需要迁移的数据库。")
            return True
            
    except Exception as e:
        print(f"检查迁移状态时出错: {e}")
        return True
    finally:
        db.close()

if __name__ == "__main__":
    print("=" * 50)
    print("用户类型和邀请码特权功能 - 数据库迁移工具")
    print("=" * 50)
    
    # 检查是否需要迁移
    if not check_migration_needed():
        sys.exit(0)
    
    # 确认迁移
    response = input("\n是否继续执行数据库迁移？(y/N): ")
    if response.lower() != 'y':
        print("迁移已取消。")
        sys.exit(0)
    
    try:
        migrate_database()
        print("\n迁移成功完成！")
    except Exception as e:
        print(f"\n迁移失败: {e}")
        print("请检查错误信息并重试。")
        sys.exit(1)