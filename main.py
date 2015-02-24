import time
import threading
import wx

from selenium import webdriver


class Window(wx.Frame):
    def __init__(self, *args, **kwargs):
        wx.Frame.__init__(self, *args, **kwargs)
        self.initialize_ui()
        self.Show()

    def initialize_ui(self):
        self.panel = wx.Panel(self)
        self.sizer = wx.BoxSizer(wx.VERTICAL)

        self.username_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.username_label = wx.StaticText(parent=self.panel,
                                            label="Username:")
        self.username = wx.TextCtrl(parent=self.panel)
        self.username_sizer.Add(self.username_label,
                                flag=wx.ALIGN_CENTER | wx.RIGHT,
                                border=10)
        self.username_sizer.Add(self.username,
                                flag=wx.ALIGN_CENTER)
        self.sizer.Add(self.username_sizer,
                       proportion=1,
                       flag=wx.EXPAND | wx.ALIGN_CENTER | wx.LEFT | wx.RIGHT,
                       border=5)

        self.password_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.password_label = wx.StaticText(parent=self.panel,
                                            label="Password:")
        self.password = wx.TextCtrl(parent=self.panel, style=wx.TE_PASSWORD)
        self.password_sizer.Add(self.password_label,
                                flag=wx.ALIGN_CENTER | wx.RIGHT,
                                border=10)
        self.password_sizer.Add(self.password,
                                flag=wx.ALIGN_CENTER)
        self.sizer.Add(self.password_sizer,
                       proportion=1,
                       flag=wx.EXPAND | wx.ALIGN_CENTER | wx.LEFT | wx.RIGHT,
                       border=5)

        self.start_button = wx.Button(parent=self.panel, label="Start!")
        self.sizer.Add(self.start_button,
                       proportion=1,
                       flag=wx.EXPAND | wx.ALIGN_CENTER)

        self.start_button.Bind(wx.EVT_BUTTON, self.on_start)

        self.panel.SetSizer(self.sizer)

    def on_start(self, event):
        self.session = Session(self.username.GetValue(),
                               self.password.GetValue())
        self.session.start()


class Session(threading.Thread):
    def __init__(self, username, password, length=300):
        threading.Thread.__init__(self)

        self.length = length

        self.browser_location = ""
        self.browser = webdriver.Chrome(self.browser_location)
        self.browser.maximize_window()
        self.browser.get("https://membean.com/login")

        user_field = self.browser.find_element_by_id("login_session_login")
        pass_field = self.browser.find_element_by_id("login_session_password")

        user_field.send_keys(username)
        pass_field.send_keys(password)

        # Submit the Form
        user_field.submit()

    def wait(self):
        wait_time = 2
        time.sleep(wait_time)

    def run(self):
        end_time = time.time() + self.length
        self.wait()
        start = self.browser.find_element_by_id("start-button")
        start.click()

        self.wait()
        proceed = self.browser.find_element_by_id("Proceed")
        proceed.click()

        while time.time() < end_time:
            if len(self.browser.find_elements_by_id("next-btn")) > 0:
                time.sleep(4)
                answer = self.browser.find_element_by_class_name("answer")
                answer.click()
                next_button = self.browser.find_element_by_id("next-btn")
                next_button.click()
            elif len(self.browser.find_elements_by_id("full-answer")) > 0:
                answer_field = self.browser.find_element_by_id("full-answer")
                answer = answer_field.get_attribute("innerHTML")
                choice = self.browser.find_element_by_id("choice")
                if len(self.browser.find_elements_by_id("word-hint")) > 0:
                    choice.send_keys(answer[1:])
                else:
                    choice.send_keys(answer)
            elif len(self.browser.find_elements_by_class_name("answer")) > 0:
                answer = self.browser.find_element_by_class_name("answer")
                answer.click()
            self.wait()
            continue

        stop = self.browser.find_element_by_id("done-btn")
        stop.click()


if __name__ == "__main__":
    app = wx.App(redirect=True, filename="log.txt")
    window = Window(parent=None,
                    title="Pybean",
                    size=(200, 150))
    app.MainLoop()
