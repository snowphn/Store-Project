#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数据库修复脚本
用于添加缺失的数据库列
"""

import sqlite3
import os
from pathlib import Path

def fix_database():
    """修复数据库，添加缺失的列"""
    
    # 数据库文件路径
    db_path = Path(__file__).parent / 'csgo_shop.db'
    
    if not db_path.exists():
        print(f"数据库文件不存在: {db_path}")
        return False
    
    try:
        # 连接数据库
        conn = sqlite3.connect(str(db_path))
        cursor = conn.cursor()
        
        print("开始修复数据库...")
        
        # 检查invite_codes表是否存在
        cursor.execute("""
            SELECT name FROM sqlite_master 
            WHERE type='table' AND name='invite_codes'
        """)
        
        if not cursor.fetchone():
            print("创建invite_codes表...")
            cursor.execute("""
                CREATE TABLE invite_codes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    code VARCHAR(20) UNIQUE NOT NULL,
                    privilege_type VARCHAR(10) DEFAULT 'normal' NOT NULL,
                    is_used BOOLEAN DEFAULT 0,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    used_at DATETIME,
                    used_by_user_id INTEGER
                )
            """)
            print("invite_codes表创建成功")
        else:
            print("invite_codes表已存在")
            
            # 检查并添加缺失的列
            cursor.execute("PRAGMA table_info(invite_codes)")
            columns = [column[1] for column in cursor.fetchall()]
            
            if 'privilege_type' not in columns:
                print("添加privilege_type列...")
                cursor.execute("""
                    ALTER TABLE invite_codes 
                    ADD COLUMN privilege_type VARCHAR(10) DEFAULT 'normal' NOT NULL
                """)
                print("privilege_type列添加成功")
            
            if 'used_by_user_id' not in columns:
                print("添加used_by_user_id列...")
                cursor.execute("""
                    ALTER TABLE invite_codes 
                    ADD COLUMN used_by_user_id INTEGER
                """)
                print("used_by_user_id列添加成功")
        
        # 检查users表
        cursor.execute("""
            SELECT name FROM sqlite_master 
            WHERE type='table' AND name='users'
        """)
        
        if cursor.fetchone():
            print("检查users表...")
            cursor.execute("PRAGMA table_info(users)")
            columns = [column[1] for column in cursor.fetchall()]
            
            if 'user_type' not in columns:
                print("添加user_type列...")
                cursor.execute("""
                    ALTER TABLE users 
                    ADD COLUMN user_type VARCHAR(10) DEFAULT 'normal' NOT NULL
                """)
                print("user_type列添加成功")
            
            if 'display_name' not in columns:
                print("添加display_name列...")
                cursor.execute("""
                    ALTER TABLE users 
                    ADD COLUMN display_name VARCHAR(100)
                """)
                print("display_name列添加成功")
            
            if 'invite_code_used' not in columns:
                print("添加invite_code_used列...")
                cursor.execute("""
                    ALTER TABLE users 
                    ADD COLUMN invite_code_used VARCHAR(20)
                """)
                print("invite_code_used列添加成功")
        
        # 提交更改
        conn.commit()
        print("数据库修复完成！")
        
        # 显示表结构
        print("\n=== invite_codes表结构 ===")
        cursor.execute("PRAGMA table_info(invite_codes)")
        for column in cursor.fetchall():
            print(f"  {column[1]} ({column[2]})")
        
        print("\n=== users表结构 ===")
        cursor.execute("PRAGMA table_info(users)")
        for column in cursor.fetchall():
            print(f"  {column[1]} ({column[2]})")
        
        return True
        
    except Exception as e:
        print(f"数据库修复失败: {str(e)}")
        return False
    finally:
        if 'conn' in locals():
            conn.close()

if __name__ == "__main__":
    print("CS:GO商店数据库修复工具")
    print("=" * 30)
    
    if fix_database():
        print("\n✅ 数据库修复成功！现在可以启动应用程序了。")
    else:
        print("\n❌ 数据库修复失败！请检查错误信息。")
    
    input("\n按回车键退出...")