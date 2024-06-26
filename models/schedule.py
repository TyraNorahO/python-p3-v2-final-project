# schedule.py
import sqlite3
import datetime

class ScheduleManager:
    def __init__(self):
        self.connection = sqlite3.connect('schedule.db')
        self.cursor = self.connection.cursor()
        
    def add_schedule(self, user_id, schedule_time):
        try:
            parsed_time = datetime.datetime.strptime(schedule_time, '%Y-%m-%d %H:%M')
            self.cursor.execute('INSERT INTO schedule (user_id, time) VALUES (?, ?)',
                                (user_id, parsed_time))
            self.connection.commit()
            print(f"Added schedule for User ID: {user_id} at {parsed_time}")
        except ValueError:
            print("Invalid date format. Please use 'YYYY-MM-DD HH:MM'")
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")

    def view_schedules(self):
        self.cursor.execute('SELECT * FROM schedule')
        schedules = self.cursor.fetchall()
        if schedules:
            for schedule in schedules:
                print(f"Schedule ID: {schedule[0]}, User ID: {schedule[1]}, Time: {schedule[2]}")
        else:
            print("No schedules found.")

    def delete_schedule(self, schedule_id):
        try:
            self.cursor.execute('DELETE FROM schedule WHERE id = ?', (schedule_id,))
            self.connection.commit()
            print(f"Deleted schedule with ID: {schedule_id}")
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")

    def update_schedule(self, schedule_id, new_time):
        try:
            parsed_time = datetime.datetime.strptime(new_time, '%Y-%m-%d %H:%M')
            self.cursor.execute('UPDATE schedule SET time = ? WHERE id = ?', 
                                (parsed_time, schedule_id))
            self.connection.commit()
            print(f"Updated schedule ID: {schedule_id} to new time: {parsed_time}")
        except ValueError:
            print("Invalid date format. Please use 'YYYY-MM-DD HH:MM'")
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")

    def find_schedule(self, user_id=None, time=None):
        try:
            if user_id is not None and time is not None:
                parsed_time = datetime.datetime.strptime(time, '%Y-%m-%d %H:%M')
                self.cursor.execute('SELECT * FROM schedule WHERE user_id = ? AND time = ?', 
                                    (user_id, parsed_time))
            elif user_id is not None:
                self.cursor.execute('SELECT * FROM schedule WHERE user_id = ?', (user_id,))
            elif time is not None:
                parsed_time = datetime.datetime.strptime(time, '%Y-%m-%d %H:%M')
                self.cursor.execute('SELECT * FROM schedule WHERE time = ?', (parsed_time,))
            else:
                print("Please provide at least one search criterion: user_id or time.")
                return []

            schedules = self.cursor.fetchall()
            if schedules:
                for schedule in schedules:
                    print(f"Schedule ID: {schedule[0]}, User ID: {schedule[1]}, Time: {schedule[2]}")
            else:
                print("No schedules found with the given criteria.")
            return schedules
        except ValueError:
            print("Invalid date format. Please use 'YYYY-MM-DD HH:MM'")
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")
            return []

    def close(self):
        self.connection.close()

if __name__ == "__main__":
    manager = ScheduleManager()
    # Example usage
    manager.add_schedule(1, '2024-12-25 09:00')
    manager.view_schedules()
    manager.update_schedule(1, '2024-12-25 10:00')
    manager.find_schedule(user_id=1)
    manager.delete_schedule(1)
    manager.view_schedules()
    manager.close()
