import requests
import pandas as pd
from common import *
from PIL import Image
import streamlit as st
from io import BytesIO
from githubqa.get_info_from_api import (
    get_repo_list, get_avatar_info,
    get_language_list, get_contributors,
    get_followers, get_commits,
    get_git_stats, get_used_language
)
from streamlit_elements import elements, mui
from streamlit_elements import nivo

# pip install streamlit-elements # streamlit-elements==0.1.0

initialize_session()
buy_me_tea()

st.title('`Search User\'s Repo`')

st.session_state["user_name"] = st.sidebar.text_input(
    'GitHub User:',  key="github_user_input_search_whois", 
    value=st.session_state["user_name"],
    on_change=handling_user_change
    )

if st.session_state["user_name"]:
    user_name = st.session_state["user_name"] # 입력된 user 이름
    repo_info = get_repo_list(user_name)
    repo_list = repo_info[0] # user의 repo list
    user_info = get_avatar_info(user_name) # user 모든 정보
    avatar_url = user_info['avatar_url']+'.png' # user 프로필 사진
    image_response = requests.get(avatar_url)
    image = Image.open(BytesIO(image_response.content)).resize((250,250))
    st.sidebar.image(image, use_column_width='always', caption=f"{user_name}'s profile")
    followers_name = get_followers(user_name)[0] # user의 팔로워
    stats = get_git_stats(user_name) # Git stats Information
    git_stats = [stats[3].strip(), stats[6], stats[7]] # Git Rank & Total Commits
    
    # ======= User Info Table ========
    st.subheader("User Info")
    
    df = pd.DataFrame(
        {
            "avartar": avatar_url,
            # "e-mail": user_info['email'],
            "git rank" : git_stats[0],
            "total repos": user_info['public_repos'],
            "total commits":git_stats[2],
            "followers": [followers_name],
        }
    )
    
    st.dataframe(
        df,
        column_config={
            "avartar": st.column_config.ImageColumn("🤡 avartar", help="User's Github Avartar"),
            # "e-mail": "📧 e-mail",
            "git rank": "🎖️ Git Rank",
            "total repos": "👝 Total Repos",
            "total commits": "💻 "+git_stats[1][:-1],
            "followers": "🤝 followers",
        },
        hide_index=True,
        
    )

    # ============= Most Used Languages ============
    with st.expander("See " + user_name.upper() + " 's frequently used Languages "):
        with elements("nivo_charts"):
            used_lang = get_used_language(user_name)
            lang_cnt = len(used_lang)//2
            DATA = [{"id":used_lang[i*2-1],"value":float(used_lang[i*2][:-1])} for i in range(1,lang_cnt+1)]

            with mui.Box(sx={"height": 300}):
                nivo.Pie(
                    data=DATA,
                    indexBy= "HI",
                    margin={ "top": 40, "right": 80, "bottom": 80, "left": 80 },
                    innerRadius=0.3,
                    padAngle=0.7,
                    cornerRadius=3,
                    activeOuterRadiusOffset=8,
                    borderWidth=1,
                    borderColor= [{"from": "color"},
                                {"modifiers": {'darker', 0.2}},
                                ],
                    arcLinkLabelsSkipAngle=10,
                    arcLinkLabelsTextColor="#333333",
                    arcLinkLabelsThickness=2,
                    arcLinkLabelsColor={"from": 'color'},
                    arcLabelsSkipAngle=10,
                    arcLabelsTextColor=[
                        {"from": "color"},
                        {"modifiers": {'darker', 0.2}},
                        ],
                    defs=[
                        {
                            'id': 'dots',
                            'type': 'patternDots',
                            'background': 'inherit',
                            'color': 'rgba(255, 255, 255, 0.3)',
                            'size': 4,
                            'padding': 1,
                            'stagger': True
                        },
                        {
                            'id': 'lines',
                            'type': 'patternLines',
                            'background': 'inherit',
                            'color': 'rgba(255, 255, 255, 0.3)',
                            'rotation': -45,
                            'lineWidth': 6,
                            'spacing': 10
                        }
                    ],
                    fill=[
                        {
                            "match": {
                                "id": 'ruby'
                            },
                            "id": 'dots'
                        },
                        {
                            "match": {
                                "id": 'c'
                            },
                            "id": 'dots'
                        },
                        {
                            "match": {
                                "id": 'go'
                            },
                            "id": 'dots'
                        },
                        {
                            "match": {
                                "id": 'python'
                            },
                            "id": 'dots'
                        },
                        {
                            "match": {
                                "id": 'scala'
                            },
                            "id": 'lines'
                        },
                        {
                            "match": {
                                "id": 'lisp'
                            },
                            "id": 'lines'
                        },
                        {
                            "match": {
                                "id": 'elixir'
                            },
                            "id": 'lines'
                        },
                        {
                            "match": {
                                "id": 'javascript'
                            },
                            "id": 'lines'
                        }
                    ],
                    legends=[
                        {
                            "anchor": "right",
                            "direction": "column",
                            "justify": False,
                            "itemWidth": 50,
                            "itemHeight": 18,
                            "itemTextColor": "#999",
                            "itemDirection": "left-to-right",
                            "itemOpacity": 1,
                            "symbolShape": "circle",
                            "effects": [
                                {
                                    "on": "hover",
                                    "style": {
                                        "itemTextColor": "#000"
                                    }
                                }
                            ],
                        }
                    ],
                )
            

    if repo_list:
        # ======= All Repo Info Table ========
        with st.spinner('Getting User Information...'):
            st.subheader("User's Repositories")
            repo_name = [repo for repo  in repo_list if repo !=DEFAULT_SELECT_VALUE]
            languages = [get_language_list(user_name, repo) for repo in repo_name]
            contributors = [get_contributors(user_name, repo)[0] for repo in repo_name]
            forks = [fork for fork in repo_info[3]]
            stars = [star for star in repo_info[2]]
            repo_url = [url for url in repo_info[1]]
        
        # 날짜 별 commit 수 flow chart
        with st.spinner('Getting repo commit Information...'):
            commits = [get_commits(user_name, repo) for repo in repo_name]
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
                "url": repo_url,
                "stars": stars,
                "commits_history": [[commit[1] for commit in commits] for commits in commit_list],
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
                "commits_history": st.column_config.LineChartColumn(
                    "Commits", y_min=0, y_max=30
                ),
                "contributers": "Contributors",
                "language": "Languages",
            },
            hide_index=True,
        )
    else:
        st.error("Invalid user ID")