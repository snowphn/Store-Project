import hashlib
import os
import hmac

def generate_salt():
    """生成随机盐值"""
    return os.urandom(16).hex()

def hash_password(password, salt=None):
    """对密码进行哈希处理
    
    Args:
        password: 原始密码
        salt: 盐值，如果为None则生成新的盐值
        
    Returns:
        (哈希后的密码, 盐值)
    """
    if salt is None:
        salt = generate_salt()
    
    # 使用SHA-256进行哈希
    hashed = hashlib.sha256((password + salt).encode()).hexdigest()
    return hashed, salt

def verify_password(password, hashed_password, salt):
    """验证密码
    
    Args:
        password: 原始密码
        hashed_password: 哈希后的密码
        salt: 盐值
        
    Returns:
        密码是否正确
    """
    return hash_password(password, salt)[0] == hashed_password

def verify_password_hmac(password: str, stored_hash: str) -> bool:
    """验证密码是否正确"""
    try:
        # 分离盐值和密钥
        salt_hex, key_hex = stored_hash.split(':')
        salt = bytes.fromhex(salt_hex)
        stored_key = bytes.fromhex(key_hex)
        
        # 使用相同的盐值和算法计算密码的哈希值
        key = hashlib.pbkdf2_hmac(
            'sha256',
            password.encode('utf-8'),
            salt,
            100000  # 迭代次数
        )
        
        # 使用 hmac.compare_digest 进行安全的比较
        return hmac.compare_digest(key, stored_key)
    except Exception:
        return False 