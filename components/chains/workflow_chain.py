# encoding:utf-8
from common import log
from typing import List, Dict
import tiktoken
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.chains.base import Chain
from common.utils import get_openai_api_key
from components.chains.utils.stream_callback import ThreadedGenerator, StreamingGeneratorCallbackHandler
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from common import log


class WorkflowChain(Chain):
    token_generator: ThreadedGenerator
    model_class = ChatOpenAI
    chain_class = LLMChain
    model_name = "gpt-3.5-turbo-16k"
    temperature = 0.75
    max_tokens = 16000
    prompt = PromptTemplate(
        input_variables=["requirement", "components"],
        template="""
system: you are a tech lead who's good at explaining software workflow, your goal is the help user to return a closed-loop data flow given the requirements and compnents. Make sure steps are detailed and the process flow is clear and comprehensive. Only return the steps.   
This is an example
requirement:
build wechat

components:
Chat Interface: Provides a user-friendly interface for users to send and receive messages within the WeChat platform.\nUser Authentication: Handles the login and verification process to ensure secure access to user accounts.\nContact Management: Manages and displays a user's contacts list for easy communication and connection with other users.\nMessaging: Allows users to send text, voice, image, and video messages to individuals or groups.\nMoment Sharing: Enables users to share photos, videos, and text updates with their contacts, similar to a social media feed.\nVoice and Video Calling: Facilitates real-time voice and video calls between users within the WeChat platform.\nPayment and Transactions: Integrates with various payment methods to enable users to make transactions, send/receive money, and pay for services.\nMini Programs: Allows users to access and use third-party applications within the WeChat ecosystem, such as games, utilities, and services.\nLocation Sharing: Enables users to share their real-time location with contacts and find nearby services or friends.\nOfficial Accounts: Provides a platform for businesses, organizations, and celebrities to create and manage their official accounts, allowing them to share news, updates, and promotional content with their followers.

User: Can you give me detailed steps of how data flow in a closed loop between all components?
You:
```
1. User opens the WeChat application on their device and logs in using their username and password.\n2. The User Authentication component receives the login request and verifies the user's credentials.\n3. Once the user is authenticated, the Chat Interface component is displayed, showing the user's contacts list.\n4. The Contact Management component retrieves the user's contacts from the database and displays them in the Chat Interface.\n5. The user selects a contact to chat with and sends a text message.\n6. The Messaging component receives the message and stores it in the database.\n7. The Messaging component also notifies the recipient's device about the new message.\n8. The recipient's device retrieves the new message from the database and displays it in their Chat Interface.\n9. The recipient can then send a reply message, and the process repeats.\n10. If the user wants to share a photo, they select the Moment Sharing option.\n11. The user's device accesses the camera or photo gallery to capture/select the photo.\n12. The photo data is then sent to the Moment Sharing component, which stores it in the database.\n13. The Moment Sharing component updates the user's contacts' feeds, showing the shared photo.\n14. If the user wants to make a voice or video call, they select the Voice and Video Calling option.\n15. The Voice and Video Calling component establishes a real-time connection between the user and the recipient's device.\n16. The voice or video data is transmitted between the devices in real-time.\n17. If the user wants to make a payment, they select the Payment and Transactions option.\n18. The Payment and Transactions component integrates with the selected payment method and processes the transaction.\n19. The transaction data is securely transmitted to the recipient's payment provider.\n20. If the user wants to use a Mini Program, they select the desired Mini Program from within WeChat.\n21. The Mini Program component loads the selected program and displays its interface within WeChat.\n22. The user interacts with the Mini Program, and any data generated within the program is stored in the Mini Program's database.\n23. If the user wants to share their location, they select the Location Sharing option.\n24. The user's device accesses the device's location services and retrieves the user's current location.\n25. The location data is sent to the Location Sharing component, which stores it in the database.\n26. The location data is then shared with the user's selected contacts.\n27. If the user wants to follow an Official Account, they search for the account and select the Follow option.\n28. The Official Accounts component updates the user's account list and displays the account's news and updates.\n29. The Official Accounts component also notifies the account owner about the new follower.\n30. The account owner can then send promotional content to their followers, and the process repeats.\n.
```

Now
requirement:
{requirement}

components:
{components}
User: Can you give me detailed steps of how data flow in a closed loop between all components?
You:
""",
    )

    @property
    def input_keys(self) -> List[str]:
        return ["requirement", "components"]

    @property
    def output_keys(self) -> List[str]:
        return ["response"]

    def _call(self, inputs: Dict[str, str]) -> Dict[str, str]:
        encoding = tiktoken.encoding_for_model(self.model_name)
        prompted_input = self.prompt.format(**inputs)
        num_tokens = len(encoding.encode(prompted_input))

        llm = self.model_class(
            temperature=self.temperature,
            openai_api_key=get_openai_api_key(),
            model_name=self.model_name,
            max_tokens=self.max_tokens - num_tokens,
            streaming=True, callback_manager=CallbackManager([StreamingGeneratorCallbackHandler(self.token_generator), StreamingStdOutCallbackHandler()])
        )

        chain = self.chain_class(prompt=self.prompt, llm=llm, verbose=False)
        outputs = {"response": chain.run(inputs)}
        self.token_generator.close()
        log.info("[WorkflowChain] output - {0}".format(outputs))
        return outputs
