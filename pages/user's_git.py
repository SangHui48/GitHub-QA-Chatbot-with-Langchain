import streamlit as st
import pandas as pd
from pages.file_viewer import print_directory_structure
from githubqa.get_info_from_api import get_repo_list, get_avatar_info
from githubqa.get_info_from_api import get_language_list, get_contributors, get_forks, get_followers, get_stars, get_commits

user = st.text_input('GitHub User:', key="github_user_input")
if user:
    repo_list = get_repo_list(user)
    user_info = get_avatar_info(user)
    avatar_url = user_info['avatar_url']+'.png'

    # ======= User Info Table ========
    followers_name = get_followers(user)[0]
    followers_url = get_followers(user)[1]

    df = pd.DataFrame(
        {
            "avartar": avatar_url,
            "e-mail": user_info['email'],
            "total repos": len(repo_list[0]),
            "followers": [followers_name],
        }
    )
    
    
    st.dataframe(
        df,
        column_config={
            "avartar": st.column_config.ImageColumn("🤡 avartar", help="User's Github Avartar"),
            "e-mail": "📧 e-mail",
            "total repos": "👝 total repos",
            "followers": "🤝 followers"
        },
        hide_index=True,
    )

    if repo_list:
        specific_repo = st.selectbox(f"Select {user}'s repository", repo_list[0], key="repo_select")

        
        # ======= All Repo Info Table ========
        repo_name = [repo for repo in repo_list[0]]
        languages = [get_language_list(user, repo) for repo in repo_name]
        contributors = [get_contributors(user, repo)[0] for repo in repo_name]
        forks = [get_forks(user, repo) for repo in repo_name]
        stars = [get_stars(user, repo) for repo in repo_name]
        
        # 날짜 별 commits 흐름
        commits = [get_commits(user, repo) for repo in repo_name]
        commit_list = []
        for i in range(len(commits)):
            commits_dict={}
            for j in range(len(commits[i])):
                commit_date = commits[i][j]['commit']['author']['date'][:10]
                if commits_dict.get(commit_date): commits_dict[commit_date] += 1
                else: commits_dict[commit_date] = 1
            commits_dict = sorted(commits_dict.items())
            commit_list.append(commits_dict)
            
        df = pd.DataFrame(
            {
                "name": repo_name,
                "url": [repo for repo in repo_list[1]],
                "stars": stars,
                "views_history": [[commit[1] for commit in commits] for commits in commit_list],
                "contributers": contributors,
                "language": languages,
            }
        )

        st.dataframe(
            df,
            column_config={
                "name": "GitHub name",
                "stars": st.column_config.NumberColumn(
                    "GitHub Stars",
                    help="Number of stars on GitHub",
                    format="%d ⭐",
                ),
                "url": st.column_config.LinkColumn("GitHub URL"),
                "views_history": st.column_config.LineChartColumn(
                    "Views (past 30 days)", y_min=0, y_max=30
                ),
                "contributers": "contributors",
                "language": "languages",
            },
            hide_index=True,
        )

        # ===================
        print_directory_structure(user, specific_repo)
    else:
        st.error("Invalid user ID")