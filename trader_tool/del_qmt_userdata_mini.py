import os
import sys
import schedule
import time
class del_qmt_userdata_mini:
    def __init__(self,folder_path=r'D:/国金QMT交易端模拟/userdata_mini',
            ):
        '''
        清空qmt缓存数据
        folder_path qmt路径
        '''
        self.folder_path=folder_path
    def delete_down_files(self,folder_path):
        """
        删除文件夹下所有以 "down" 开头的文件（不处理子文件夹）
        :param folder_path: 目标文件夹路径
        
        """
        deleted_files = []
        failed_files = []

        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)
            
            # 仅处理文件（跳过文件夹），并且文件名以 "down" 开头（不区分大小写）
            if os.path.isfile(file_path) and filename.lower().startswith("down"):
                try:
                    os.unlink(file_path)  # 删除文件
                    deleted_files.append(filename)
                    print(f"✅ 已删除: {filename}")
                except PermissionError:
                    failed_files.append((filename, "权限不足"))
                except Exception as e:
                    failed_files.append((filename, str(e)))
        
        # 输出结果汇总
        print("\n=== 操作结果 ===")
        print(f"成功删除: {len(deleted_files)} 个文件")
        if failed_files:
            print("\n以下文件删除失败:")
            for file, reason in failed_files:
                print(f"❌ {file} ({reason})")

    def validate_folder_path(self,folder_path):
        """验证文件夹路径是否存在"""
        if not os.path.exists(folder_path):
            print(f"错误: 文件夹 '{folder_path}' 不存在！")
            sys.exit(1)
        if not os.path.isdir(folder_path):
            print(f"错误: '{folder_path}' 不是有效文件夹！")
            sys.exit(1)

    def del_all_qmt_folder(self,):
        '''
        删除全部的qmt文件
        '''
        # 配置目标路径（请修改为实际路径）
        target_folder = self.folder_path
        
        # 1. 验证路径有效性
        self.validate_folder_path(target_folder)
        
        # 2. 执行删除操作
        print(f"\n🛠️ 正在清理文件夹: {target_folder}")
        self.delete_down_files(target_folder)
        
        # 3. 防止窗口闪退（仅调试时使用）
        #input("\n按回车键退出..." if "--debug" in sys.argv else "")
    
    
if __name__ == "__main__":
    models=del_qmt_userdata_mini(folder_path=r'D:/国金QMT交易端模拟/userdata_mini')
    models.del_all_qmt_folder()
