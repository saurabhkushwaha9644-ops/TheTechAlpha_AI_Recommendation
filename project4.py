import streamlit as st

item_dataset = {
    "The Hobbit": ["Fantasy", "Adventure", "Fiction"],
    "Harry Potter": ["Fantasy", "Magic", "Adventure"],
    "Sherlock Holmes": ["Mystery", "Detective", "Fiction"],
    "Murder on the Orient Express": ["Mystery", "Thriller"],
    "Dune": ["Sci-Fi", "Space", "Adventure"],
    "Neuromancer": ["Sci-Fi", "Cyberpunk"],
    "The Notebook": ["Romance", "Drama", "Fiction"],
    "Pride and Prejudice": ["Romance", "Classic", "Drama"]
}

def calculate_similarity(item1, item2):
    features1 = item_dataset[item1]
    features2 = item_dataset[item2]
    shared = set(features1).intersection(features2)
    return len(shared)

def get_bot_recommendations(chosen_item, top_n=3):
    if chosen_item not in item_dataset:
        return None

    similarity_list = []
    for item_name in item_dataset.keys():
        if item_name == chosen_item:
            continue
        
        score = calculate_similarity(chosen_item, item_name)
        if score > 0:
            similarity_list.append((item_name, score))
            
    similarity_list.sort(key=lambda x: x[1], reverse=True)
    return similarity_list[:top_n]

st.set_page_config(page_title="AI Recommendation Assistant", page_icon="🤖")

st.title("🤖 AI Recommendation Chatbot")
st.write("Welcome! I am your content-based recommendation assistant built for Task 4.")
st.markdown("---")

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hello! Select a book from the sidebar or type its name here to get matching recommendations. You can also click 'Show Available Books' to see the database!"}
    ]

with st.sidebar:
    st.header("Database Operations")
    if st.button("📚 Show Available Books"):
        st.write("### Current Inventory:")
        for title in item_dataset.keys():
            st.write(f"- {title} *({', '.join(item_dataset[title])})*")
    
    st.markdown("---")
    selected_option = st.selectbox("Quick Select a Book:", [""] + list(item_dataset.keys()))
    if selected_option:
        st.session_state.quick_pick = selected_option

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

user_input = st.chat_input("Type a book name...")

if "quick_pick" in st.session_state and st.session_state.quick_pick:
    user_input = st.session_state.quick_pick
    del st.session_state.quick_pick

if user_input:
    with st.chat_message("user"):
        st.write(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    matched_item = None
    for title in item_dataset.keys():
        if user_input.lower() == title.lower():
            matched_item = title
            break
            
    with st.chat_message("assistant"):
        if matched_item:
            response_text = f"Great choice! I see you like '{matched_item}'. Processing features..."
            st.write(response_text)
            
            recommendations = get_bot_recommendations(matched_item)
            if not recommendations:
                bot_reply = "I analyzed all tags, but unfortunately, I couldn't find any similar items right now."
                st.write(bot_reply)
            else:
                bot_reply = f"Based on the content features, here are my top suggestions for '{matched_item}':\n\n"
                for rank, (item, score) in enumerate(recommendations, start=1):
                    bot_reply += f"{rank}. **{item}** (Match Score: {score})\n"
                st.write(bot_reply)
        else:
            bot_reply = f"I couldn't find '{user_input}' in my dataset. Click 'Show Available Books' in the sidebar to check the correct spellings."
            st.write(bot_reply)
            
    st.session_state.messages.append({"role": "assistant", "content": bot_reply})
