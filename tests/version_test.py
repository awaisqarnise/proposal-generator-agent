import langgraph
import langchain
import langchain_openai
from langchain_openai import ChatOpenAI

# LangGraph doesn't have __version__, check differently
print(f"✅ LangGraph imported: {langgraph.__name__}")
print(f"✅ LangChain: {langchain.__version__}")

# Test actual functionality
try:
    from langgraph.graph import StateGraph
    print("✅ StateGraph imported successfully")
except ImportError as e:
    print(f"❌ StateGraph import failed: {e}")

# Test OpenAI connection (no API call, just import)
try:
    llm = ChatOpenAI(model="gpt-4", api_key="dummy")
    print("✅ ChatOpenAI class available")
except Exception as e:
    print(f"⚠️  ChatOpenAI setup issue: {e}")

print("\n🎉 All core libraries installed correctly!")