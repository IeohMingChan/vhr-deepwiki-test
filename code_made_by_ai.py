```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
学生成绩管理系统 - 1000行Python代码示例
作者: 研发云智能助手CodeFree
功能: 实现学生信息的增删改查、成绩统计、数据持久化等
"""

import json
import os
import datetime
from typing import Dict, List, Optional, Tuple


class Student:
    """学生类，存储学生基本信息和成绩"""
    
    def __init__(self, student_id: str, name: str, age: int, gender: str):
        """
        初始化学生对象
        
        Args:
            student_id: 学号
            name: 姓名
            age: 年龄
            gender: 性别
        """
        self.student_id = student_id
        self.name = name
        self.age = age
        self.gender = gender
        self.scores = {}  # 科目-成绩字典
        self.create_time = datetime.datetime.now()
    
    def add_score(self, subject: str, score: float) -> bool:
        """
        添加或更新成绩
        
        Args:
            subject: 科目名称
            score: 成绩分数
            
        Returns:
            bool: 操作是否成功
        """
        if not isinstance(score, (int, float)) or score < 0 or score > 100:
            return False
        
        self.scores[subject] = score
        return True
    
    def get_average_score(self) -> float:
        """
        计算平均分
        
        Returns:
            float: 平均分，如果没有成绩返回0.0
        """
        if not self.scores:
            return 0.0
        return sum(self.scores.values()) / len(self.scores)
    
    def get_total_score(self) -> float:
        """
        计算总分
        
        Returns:
            float: 总分
        """
        return sum(self.scores.values())
    
    def to_dict(self) -> Dict:
        """
        将学生对象转换为字典
        
        Returns:
            Dict: 学生信息字典
        """
        return {
            'student_id': self.student_id,
            'name': self.name,
            'age': self.age,
            'gender': self.gender,
            'scores': self.scores,
            'create_time': self.create_time.isoformat()
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'Student':
        """
        从字典创建学生对象
        
        Args:
            data: 学生数据字典
            
        Returns:
            Student: 学生对象
        """
        student = cls(
            data['student_id'],
            data['name'],
            data['age'],
            data['gender']
        )
        student.scores = data.get('scores', {})
        student.create_time = datetime.datetime.fromisoformat(data['create_time'])
        return student
    
    def __str__(self) -> str:
        """返回学生信息的字符串表示"""
        avg_score = self.get_average_score()
        return (f"学号: {self.student_id}, 姓名: {self.name}, 年龄: {self.age}, "
                f"性别: {self.gender}, 平均分: {avg_score:.2f}")


class StudentManager:
    """学生管理类，负责学生数据的增删改查和持久化"""
    
    def __init__(self, data_file: str = "students_data.json"):
        """
        初始化学生管理器
        
        Args:
            data_file: 数据文件路径
        """
        self.data_file = data_file
        self.students: Dict[str, Student] = {}  # 学号到学生对象的映射
        self.load_data()
    
    def add_student(self, student: Student) -> bool:
        """
        添加学生
        
        Args:
            student: 学生对象
            
        Returns:
            bool: 添加是否成功
        """
        if student.student_id in self.students:
            return False
        
        self.students[student.student_id] = student
        self.save_data()
        return True
    
    def delete_student(self, student_id: str) -> bool:
        """
        删除学生
        
        Args:
            student_id: 学号
            
        Returns:
            bool: 删除是否成功
        """
        if student_id not in self.students:
            return False
        
        del self.students[student_id]
        self.save_data()
        return True
    
    def update_student(self, student_id: str, **kwargs) -> bool:
        """
        更新学生信息
        
        Args:
            student_id: 学号
            **kwargs: 要更新的字段
            
        Returns:
            bool: 更新是否成功
        """
        if student_id not in self.students:
            return False
        
        student = self.students[student_id]
        
        # 更新基本信息
        if 'name' in kwargs:
            student.name = kwargs['name']
        if 'age' in kwargs:
            student.age = kwargs['age']
        if 'gender' in kwargs:
            student.gender = kwargs['gender']
        
        # 更新成绩
        if 'scores' in kwargs:
            for subject, score in kwargs['scores'].items():
                student.add_score(subject, score)
        
        self.save_data()
        return True
    
    def find_student(self, student_id: str) -> Optional[Student]:
        """
        查找学生
        
        Args:
            student_id: 学号
            
        Returns:
            Optional[Student]: 找到的学生对象，未找到返回None
        """
        return self.students.get(student_id)
    
    def search_students(self, keyword: str) -> List[Student]:
        """
        搜索学生（按姓名或学号模糊匹配）
        
        Args:
            keyword: 搜索关键词
            
        Returns:
            List[Student]: 匹配的学生列表
        """
        result = []
        for student in self.students.values():
            if (keyword in student.student_id or 
                keyword in student.name or 
                keyword in student.gender):
                result.append(student)
        return result
    
    def get_all_students(self) -> List[Student]:
        """
        获取所有学生
        
        Returns:
            List[Student]: 学生列表
        """
        return list(self.students.values())
    
    def get_students_by_score_range(self, min_score: float, max_score: float) -> List[Student]:
        """
        根据分数范围筛选学生
        
        Args:
            min_score: 最低平均分
            max_score: 最高平均分
            
        Returns:
            List[Student]: 符合条件的学生列表
        """
        result = []
        for student in self.students.values():
            avg_score = student.get_average_score()
            if min_score <= avg_score <= max_score:
                result.append(student)
        return result
    
    def get_class_statistics(self) -> Dict:
        """
        获取班级统计信息
        
        Returns:
            Dict: 统计信息字典
        """
        if not self.students:
            return {
                'total_students': 0,
                'average_score': 0,
                'max_score': 0,
                'min_score': 0,
                'excellent_count': 0,
                'fail_count': 0
            }
        
        total_students = len(self.students)
        scores = [student.get_average_score() for student in self.students.values()]
        
        return {
            'total_students': total_students,
            'average_score': sum(scores) / total_students,
            'max_score': max(scores),
            'min_score': min(scores),
            'excellent_count': len([s for s in scores if s >= 90]),
            'fail_count': len([s for s in scores if s < 60])
        }
    
    def save_data(self) -> bool:
        """
        保存数据到文件
        
        Returns:
            bool: 保存是否成功
        """
        try:
            data = {
                'students': {
                    sid: student.to_dict() 
                    for sid, student in self.students.items()
                }
            }
            
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            
            return True
        except Exception as e:
            print(f"保存数据失败: {e}")
            return False
    
    def load_data(self) -> bool:
        """
        从文件加载数据
        
        Returns:
            bool: 加载是否成功
        """
        if not os.path.exists(self.data_file):
            return True
        
        try:
            with open(self.data_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            self.students = {
                sid: Student.from_dict(student_data)
                for sid, student_data in data.get('students', {}).items()
            }
            
            return True
        except Exception as e:
            print(f"加载数据失败: {e}")
            return False


class GradeManagerUI:
    """成绩管理UI界面类"""
    
    def __init__(self):
        """初始化UI界面"""
        self.manager = StudentManager()
        self.menu_options = {
            '1': ('添加学生', self.add_student_ui),
            '2': ('删除学生', self.delete_student_ui),
            '3': ('修改学生信息', self.update_student_ui),
            '4': ('查询学生', self.query_student_ui),
            '5': ('添加成绩', self.add_score_ui),
            '6': ('显示所有学生', self.show_all_students_ui),
            '7': ('成绩统计', self.show_statistics_ui),
            '8': ('搜索学生', self.search_students_ui),
            '9': ('退出系统', self.exit_system)
        }
    
    def display_menu(self):
        """显示主菜单"""
        print("\n" + "=" * 50)
        print("           学生成绩管理系统")
        print("=" * 50)
        
        for key, (description, _) in self.menu_options.items():
            print(f"{key}. {description}")
        
        print("=" * 50)
    
    def add_student_ui(self):
        """添加学生界面"""
        print("\n--- 添加学生 ---")
        
        try:
            student_id = input("请输入学号: ").strip()
            if not student_id:
                print("学号不能为空!")
                return
            
            if self.manager.find_student(student_id):
                print("该学号已存在!")
                return
            
            name = input("请输入姓名: ").strip()
            if not name:
                print("姓名不能为空!")
                return
            
            age = int(input("请输入年龄: "))
            if age < 0 or age > 150:
                print("年龄必须在0-150之间!")
                return
            
            gender = input("请输入性别(男/女): ").strip()
            if gender not in ['男', '女']:
                print("性别必须是'男'或'女'!")
                return
            
            student = Student(student_id, name, age, gender)
            
            if self.manager.add_student(student):
                print("添加学生成功!")
            else:
                print("添加学生失败!")
                
        except ValueError:
            print("年龄必须是数字!")
        except Exception as e:
            print(f"发生错误: {e}")
    
    def delete_student_ui(self):
        """删除学生界面"""
        print("\n--- 删除学生 ---")
        
        student_id = input("请输入要删除的学号: ").strip()
        if not student_id:
            print("学号不能为空!")
            return
        
        student = self.manager.find_student(student_id)
        if not student:
            print("未找到该学生!")
            return
        
        print(f"找到学生: {student}")
        confirm = input("确认删除吗? (y/n): ").strip().lower()
        
        if confirm == 'y':
            if self.manager.delete_student(student_id):
                print("删除成功!")
            else:
                print("删除失败!")
        else:
            print("取消删除")
    
    def update_student_ui(self):
        """修改学生信息界面"""
        print("\n--- 修改学生信息 ---")
        
        student_id = input("请输入要修改的学号: ").strip()
        if not student_id:
            print("学号不能为空!")
            return
        
        student = self.manager.find_student(student_id)
        if not student:
            print("未找到该学生!")
            return
        
        print(f"当前信息: {student}")
        print("\n请选择要修改的内容:")
        print("1. 姓名")
        print("2. 年龄")
        print("3. 性别")
        print("4. 取消")
        
        choice = input("请选择(1-4): ").strip()
        
        update_data = {}
        try:
            if choice == '1':
                new_name = input("请输入新姓名: ").strip()
                if new_name:
                    update_data['name'] = new_name
            elif choice == '2':
                new_age = int(input("请输入新年龄: "))
                if 0 <= new_age <= 150:
                    update_data['age'] = new_age
                else:
                    print("年龄必须在0-150之间!")
                    return
            elif choice == '3':
                new_gender = input("请输入新性别(男/女): ").strip()
                if new_gender in ['男', '女']:
                    update_data['gender'] = new_gender
                else:
                    print("性别必须是'男'或'女'!")
                    return
            elif choice == '4':
                print("取消修改")
                return
            else:
                print("无效选择!")
                return
            
            if update_data and self.manager.update_student(student_id, **update_data):
                print("修改成功!")
            else:
                print("修改失败!")
                
        except ValueError:
            print("年龄必须是数字!")
        except Exception as e:
            print(f"发生错误: {e}")
    
    def query_student_ui(self):
        """查询学生界面"""
        print("\n--- 查询学生 ---")
        
        student_id = input("请输入学号: ").strip()
        if not student_id:
            print("学号不能为空!")
            return
        
        student = self.manager.find_student(student_id)
        if student:
            self.display_student_detail(student)
        else:
            print("未找到该学生!")
    
    def add_score_ui(self):
        """添加成绩界面"""
        print("\n--- 添加成绩 ---")
        
        student_id = input("请输入学号: ").strip()
        if not student_id:
            print("学号不能为空!")
            return
        
        student = self.manager.find_student(student_id)
        if not student:
            print("未找到该学生!")
            return
        
        print(f"学生: {student.name}")
        subject = input("请输入科目名称: ").strip()
        if not subject:
            print("科目名称不能为空!")
            return
        
        try:
            score = float(input("请输入成绩(0-100): "))
            if score < 0 or score > 100:
                print("成绩必须在0-100之间!")
                return
            
            if student.add_score(subject, score):
                self.manager.save_data()
                print("添加成绩成功!")
            else:
                print("添加成绩失败!")
                
        except ValueError:
            print("成绩必须是数字!")
        except Exception as e:
            print(f"发生错误: {e}")
    
    def show_all_students_ui(self):
        """显示所有学生界面"""
        print("\n--- 所有学生列表 ---")
        
        students = self.manager.get_all_students()
        if not students:
            print("暂无学生数据!")
            return
        
        # 按学号排序
        students.sort(key=lambda s: s.student_id)
        
        print(f"{'学号':<12} {'姓名':<10} {'年龄':<4} {'性别':<4} {'平均分':<8} {'科目数':<6}")
        print("-" * 60)
        
        for student in students:
            avg_score = student.get_average_score()
            subject_count = len(student.scores)
            print(f"{student.student_id:<12} {student.name:<10} {student.age:<4} "
                  f"{student.gender:<4} {avg_score:<8.2f} {subject_count:<6}")
        
        print(f"\n总计: {len(students)} 名学生")
    
    def show_statistics_ui(self):
        """显示统计信息界面"""
        print("\n--- 班级成绩统计 ---")
        
        stats = self.manager.get_class_statistics()
        
        if stats['total_students'] == 0:
            print("暂无学生数据!")
            return
        
        print(f"总学生数: {stats['total_students']}")
        print(f"班级平均分: {stats['average_score']:.2f}")
        print(f"最高分: {stats['max_score']:.2f}")
        print(f"最低分: {stats['min_score']:.2f}")
        print(f"优秀人数(≥90分): {stats['excellent_count']}")
        print(f"不及格人数(<60分): {stats['fail_count']}")
        
        # 显示分数段分布
        print("\n--- 分数段分布 ---")
        ranges = [(90, 100), (80, 89), (70, 79), (60, 69), (0, 59)]
        range_names = ['优秀', '良好', '中等', '及格', '不及格']
        
        students = self.manager.get_all_students()
        for (min_r, max_r), name in zip(ranges, range_names):
            count = len([s for s in students 
                        if min_r <= s.get_average_score() <= max_r])
            percentage = (count / stats['total_students']) * 100
            print(f"{name}({min_r}-{max_r}分): {count}人 ({percentage:.1f}%)")
    
    def search_students_ui(self):
        """搜索学生界面"""
        print("\n--- 搜索学生 ---")
        
        keyword = input("请输入搜索关键词(学号/姓名/性别): ").strip()
        if not keyword:
            print("搜索关键词不能为空!")
            return
        
        results = self.manager.search_students(keyword)
        if not results:
            print("未找到匹配的学生!")
            return
        
        print(f"找到 {len(results)} 个匹配结果:")
        print(f"{'学号':<12} {'姓名':<10} {'年龄':<4} {'性别':<4}
