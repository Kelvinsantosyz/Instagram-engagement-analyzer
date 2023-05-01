import instaloader
import matplotlib.pyplot as plt
from datetime import datetime


class InstagramAnalyzer:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.L = instaloader.Instaloader()

    def login(self):
        self.L.context.log("Logging in...")
        self.L.context.login(self.username, self.password)

    def get_profile(self, target_profile):
        self.profile = instaloader.Profile.from_username(self.L.context, target_profile)

    def analyze_posts(self, max_posts):
        self.posts_engagement = []
        self.posts_dates = []
        count = 0
        for post in self.profile.get_posts():
            if count >= max_posts:
                break
            count += 1
            likes_count = post.likes
            comments_count = post.comments
            followers_count = self.profile.followers
            engagement_rate = (likes_count + comments_count) / followers_count * 100
            self.posts_engagement.append(engagement_rate)
            date_posted = post.date_local.strftime('%Y-%m-%d %H:%M:%S')
            self.posts_dates.append(datetime.strptime(date_posted, '%Y-%m-%d %H:%M:%S'))
            print(f"A postagem {post.shortcode} foi criada em {date_posted} e tem um engajamento de {engagement_rate:.2f}%.")

    def plot_graph(self, max_posts):
        average_engagement = sum(self.posts_engagement) / len(self.posts_engagement)
        print(f'Numero de seguidores {self.profile.username}, {self.profile.followers}')
        print(f"As {max_posts} postagens mais recentes de {self.profile.username} têm um engajamento médio de {average_engagement:.2f}%.")

        plt.style.use('ggplot')
        plt.figure(figsize=(12, 6))
        plt.plot(self.posts_dates, self.posts_engagement)
        plt.grid(True)
        plt.xticks(rotation=45)
        plt.legend(["Engajamento"], loc="upper left")
        plt.title(f"Engajamento das últimas {max_posts} postagens de {self.profile.username}")
        plt.xlabel("Data")
        plt.ylabel("Taxa de Engajamento (%)")
        plt.show()


if __name__ == '__main__':
    username = input("Enter your Instagram username: ")
    password = input("Enter your Instagram password: ")
    target_profile = input("Enter your target profile: ")
    max_posts = int(input("How many posts do you want to analyze?: "))

    analyzer = InstagramAnalyzer(username, password)
    analyzer.login()
    analyzer.get_profile(target_profile)
    analyzer.analyze_posts(max_posts)
    analyzer.plot_graph(max_posts)

