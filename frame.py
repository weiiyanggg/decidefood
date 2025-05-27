from tkinter import ttk, messagebox
import csv
import tkinter as tk


class DescriptionFrame(tk.Frame):
    '''
    Describes the QuestionFrame below
    '''

    def __init__(self, controller) -> None:
        super().__init__(controller.root, bg='#7c8ba3')
        self.root = controller.root
        self.create_widgets()

    def create_widgets(self):
        desc1_label = tk.Label(self, text="🍔 INDECISIVE? DO NOT KNOW WHAT TO EAT? 🍨\n\n🍚 LET US HELP YOU! 🍟",
                               font=('Comic Sans MS', 20, "bold"), fg='white', bg='#7c8ba3', pady=90, anchor='w')
        desc1_label.pack()
        desc2_label = tk.Label(self, text="Choose from the options below!",
                               font=('Comic Sans MS', 14, "bold"), fg='white', bg='#7c8ba3', pady=10, anchor='w')
        desc2_label.pack(pady=10)


class QuestionFrame(tk.Frame):
    '''
    Contains questions for the user to answer so to obtain their preferences and recommend places to eat
    '''

    def __init__(self, controller) -> None:
        super().__init__(controller.root, bg='#7c8ba3')
        self.root = controller.root
        self.answers = {}
        self.question_gen = self.read_line('assets/questions.txt')
        self.current_question = next(self.question_gen)
        self.create_widgets()

    def read_line(self, file_path):
        with open(file_path, 'r') as file:
            for line in file:
                yield line.strip().split(': ')

    def create_widgets(self):
        self.question_label = tk.Label(self, text=self.current_question[0],
                                       font=('Comic Sans MS', 12), bg='#7c8ba3')
        self.question_label.pack(pady=10)
        self.create_buttons()

    def create_buttons(self):
        question = self.current_question[0]
        choices = self.current_question[1].split(', ')
        for choice in choices:
            button = ttk.Button(
                self, text=choice, command=lambda answer=choice.lower(), question=question: self.next_question(answer, question), style="Next.TButton")
            button.pack(side='left', padx=10, pady=30)

    def next_question(self, answer, question):
        '''
        For use by button widget when user clicks on the button
        '''
        self.answers[question] = answer
        try:
            self.current_question = next(self.question_gen)
            self.question_label.config(
                text=self.current_question[0])
            for widget in self.winfo_children():
                if isinstance(widget, ttk.Button):
                    widget.destroy()
            self.create_buttons()
        except:
            self.save_answers_to_file()
            messagebox.showinfo(
                "Recommended list of food places below!", f'{self.recommend()}')
            self.root.destroy()

    def save_answers_to_file(self):
        try:
            with open("assets/user_preferences.txt", "w") as file:
                for key, value in self.answers.items():
                    file.write(f"{key}: {value}\n")
        except (IOError, PermissionError) as e:
            messagebox.showerror(
                "Error", f"Error saving preferences to file: {e}")

    def get_dict(self):
        file_path = 'assets/places_to_eat.csv'
        with open(file_path, 'r') as csv_file:
            csv_reader = csv.reader(csv_file)
            places = {}
            for row in csv_reader:
                places[row[0]] = row[1:]
            return places

    def score(self):
        '''
        Gives each place a score based on user's answers.
        The more similarities between the user's preferences and the place, 
        the higher the score.
        '''
        pref_attrs = [value for value in self.answers.values()]
        places = self.get_dict()
        formatted_places = {}
        for place in places:
            place_split = place.split(' ')
            proper_place = ''
            for word in place_split:
                x = 0
                for l in word:
                    if l.isdigit():
                        x = 1
                        break
                if x == 1:
                    proper_place += word + ' '
                    break
                x = 0
                first = word[0]
                back = word[1:].lower()
                proper_word = first + back
                proper_place += proper_word + ' '
            formatted_places[proper_place] = places[place]
        places = formatted_places
        place_score = {}
        for place in places.keys():
            place_score[place] = 0
        for place, ls_attr in places.items():
            for attr in ls_attr:
                for pref_attr in pref_attrs:
                    if pref_attr in attr.lower():
                        place_score[place] += 1
        return place_score

    def recommend(self):
        '''
        The highest score place will be recommended
        '''
        place_score = self.score()
        top = max(place_score.values())
        recommendations = []
        for place, score in place_score.items():
            if score == top:
                recommendations.append(place)

        # Use newline characters to separate recommendations
        recommendations_formatted = "\n".join(recommendations)
        return recommendations_formatted
