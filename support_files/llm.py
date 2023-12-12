import os
import boto3

from typing import List, Mapping

import langchain
from langchain.llms.bedrock import Bedrock

from langchain.chains.llm import LLMChain
from langchain.chains.base import Chain
from langchain.chains.router.llm_router import LLMRouterChain, RouterOutputParser
from langchain.chains.router.base import MultiRouteChain, RouterChain

from langchain.chains.router.multi_prompt_prompt import MULTI_PROMPT_ROUTER_TEMPLATE
from langchain.prompts import PromptTemplate, ChatPromptTemplate

os.environ["AWS_DEFAULT_REGION"] = "us-west-2"
os.environ["BEDROCK_ENDPOINT_URL"] = "https://bedrock-runtime.us-west-2.amazonaws.com"

class MultiPromptChain(MultiRouteChain):
    router_chain: RouterChain
    destination_chains: Mapping[str, Chain]
    default_chain: Chain

    @property
    def output_keys(self) -> List[str]:
        return ["text"]



client = boto3.client(service_name = 'bedrock-runtime', 
                      region_name=os.environ.get("AWS_DEFAULT_REGION", None), 
                      endpoint_url=os.environ.get("BEDROCK_ENDPOINT_URL", None))

model = "anthropic.claude-v2"
parameter = {"max_tokens_to_sample":1024, 
             "stop_sequences":["\\n\\nHuman:","\\nHuman:","Human:",],
             "temperature":0,
             "top_k":250,
             "top_p":0}
llm = Bedrock(model_id=model, client=client, model_kwargs=parameter)

#router prompt
personal_tamplate = """I want you answer about user personal information
Here is a question:
{input}

아래의 정보가 답변에 도움이 되는 경우 활용하세요.
#비행기 예약 현황
- 가는 편
국제선
비행번호 = 7784C8
예약등급 = FLYBAG
인천(2023.12.27(수) 20:35) => 베를린(2023.12.28(목) 08:12))
- 오는 편
국제선
비행번호 = 7784C9
예약등급 = FLYBAG
베를린(2023.12.31(일) 11:35) => 인천(2023.12.31(일) 22:16))

#유의사항
국제선 탑승수속 시작시간 = 출발 2시간 30분전 시작
국제선 탑승수속 마감시간 = 출발 60분 전 마감

#사용자 마일리지 정보
마일리지: 50,000 

#마일리지 공제표(편도기준)
대한민국 (국내선) 평수기 = 일반석(5,000) 비지니스석(6,000) 일등석(없음)
대한민국 (국내선) 성수기 = 일반석(10,000) 비지니스석(16,000) 일등석(없음)
북미/유럽/중동/대양주 평수기 = 일반석(60,000) 비지니스석(160,000) 일등석(없음)
북미/유럽/중동/대양주 성수기 = 일반석(70,000) 비지니스석(200,000) 일등석(없음)

<< FORMATTING >>
Return a markdown code snippet with a JSON object formatted to look like:
```json
{{{{
    "destination": "Personal"
    "Answer": string \\ this is your final answer
}}}}
```
Assistant:"""

reservation_tamplate = """I want you answer about airline tikecting
Here is a question:
{input}

아래의 정보가 답변에 도움이 되는 경우 활용하세요.
#비행 스케줄
출발지: 인천, 도착지: 뉴욕, 출발일자: 2023-12-05, 비용: 302,343.1
출발지: 뉴욕, 도착지: 인천, 귀국일자: 2024-01-01, 비용: 198,612.7

출발지: 인천, 도착지: 뉴욕, 출발일자: 2024-01-04, 비용: 291,944.1
출발지: 뉴욕, 도착지: 인천, 귀국일자: 2023-12-01, 비용: 177,741.3

출발지: 인천, 도착지: 뉴욕, 출발일자: 2024-02-28, 비용: 288,108.0
출발지: 뉴욕, 도착지: 인천, 귀국일자: 2024-02-23, 비용: 140,098.5

출발지: 인천, 도착지: 뉴욕, 출발일자: 2024-03-27, 비용: 307,031.5
출발지: 뉴욕, 도착지: 인천, 귀국일자: 2024-03-18, 비용: 199,531.6

출발지: 인천, 도착지: 뉴욕, 출발일자: 2024-03-28, 비용: 341,484.3
출발지: 뉴욕, 도착지: 인천, 귀국일자: 2024-01-16, 비용: 130,245.4

<< FORMATTING >>
Return a markdown code snippet with a JSON object formatted to look like:
```json
{{{{
    "destination": "Reservation"
    "Answer": string \\ this is your final answer
}}}}
```
Assistant:"""
cancellation_tamplate = """I want you answer about airline tikect cancellation
Here is a question:
{input}

아래의 정보가 답변에 도움이 되는 경우 활용하세요.
#취소 수수료
한국(KRW) 60,000


<< FORMATTING >>
Return a markdown code snippet with a JSON object formatted to look like:
```json
{{{{
    "destination": "Cancellation"
    "Answer": string \\ this is your final answer
}}}}
```
Assistant:"""
modification_tamplate = """I want you answer about airline tikect Modification
Here is a question:
{input}

아래의 정보가 답변에 도움이 되는 경우 활용하세요.
#항공권 변경 정책
탑승날짜 변경만 가능하며, 이용구간(노선) 변경은 할 수 없다.

1) 국내선 항공권 날짜 변경시
- 최초 결제금액에서 변경수수료를 제외한 금액이 환불된다.
- 환불 된 이후 신규 항공권 운임으로 다시 결제 된다.

2) 국제선 항공권 날짜 변경시
- 기존 구매한 항공권과 새로 구매한 항공권 운임 차액과 변경 수수료가 추가로 결제된다.

#변경 수수료
한국(KRW) 60,000

<< FORMATTING >>
Return a markdown code snippet with a JSON object formatted to look like:
```json
{{{{
    "destination": "Modification"
    "Answer": string \\ this is your final answer
}}}}
```
Assistant:"""
FAQ_tamplate = """I want you answer about FAQ Information
Here is a question:
{input}

아래의 정보가 답변에 도움이 되는 경우 활용하세요.
#반려동물과 같이 여행할 수 있나요?
국내선의 경우 생후 8주 이상의 애완용 개, 고양이, 새에 한하여 승객과 함께 기내로 운송이 가능합니다.
(국제선도 일부 노선에서 반려동물 운송 서비스를 시행하고 있습니다.)
#탑승 후 포인트 적립 또는 누락포인트는 어떻게 적립하나요?
탑승 후 포인트 적립하기 또는 누락 포인트 적립은 탑승 완료후 6개월 이내에 진행하셔야 하며, 회원가입 및 로그인을 진행하신 뒤에 제주항공 홈페이지 > 회원혜택 > 탑승 후 적립에서 신청하시면 됩니다. 


<< FORMATTING >>
Return a markdown code snippet with a JSON object formatted to look like:
```json
{{{{
    "destination": "FAQ"
    "Answer": string \\ this is your final answer
}}}}
```
Assistant:"""

prompt_information=[
    {
        "name":"Personal",
        "description":"예약한 티켓 정보, 회원정보, 마일리지 정보를 조회하는데 사용한다.",
        "prompt_template":personal_tamplate
    },
    {
        "name":"Reservation",
        "description":"신규 티켓을 예약하는데 사용한다.",
        "prompt_template":reservation_tamplate
    },
    {
        "name":"Cancellation",
        "description":"예약 티켓을 취소할 때 사용한다.",
        "prompt_template":cancellation_tamplate
    },
    {
        "name":"Modification",
        "description":"티켓 예약 정보를 변경할 때 사용한다.",
        "prompt_template":modification_tamplate
    },
    {
        "name":"FAQ",
        "description":"사용자들이 자주 묻는 질문에 대답하기 위해서 사용한다.",
        "prompt_template":FAQ_tamplate
    }
]

MULTI_PROMPT_ROUTER_TEMPLATE = """Human: 당신은 항공사 상담원 입니다.\
Given a raw text input to a language model select the model prompt best suited for \
the input. You will be given the names of the available prompts and a description of \
what the prompt is best suited for.

<< FORMATTING >>
Return a markdown code snippet with a JSON object formatted to look like:
```json
{{{{
    "destination": string \\ name of the prompt to use or "DEFAULT"
    "next_inputs": string \\ do not modify the original input
}}}}
```

REMEMBER: "destination" MUST be one of the candidate prompt names specified below OR \
it can be "DEFAULT" if the input is not well suited for any of the candidate prompts.
REMEMBER: "next_inputs" MUST be the original input.

<< CANDIDATE PROMPTS >>
{destinations}

<< INPUT >>
{{input}}

REMEMBER: read carefully again {{input}}


<< OUTPUT (must include ```json at the start of the response) >>
<< OUTPUT (must end with ```) >>
"""


#default chain 
default_template = """Human: I want you answer about User Question
Here is a question:
{input}
Assistant:"""
default_prompt = PromptTemplate(input_variables=["input"], template=default_template)
default_chain = LLMChain(llm=llm, prompt=default_prompt)

#destination chain
destination_chains = {}
for p_info in prompt_information:
    name = p_info["name"]
    prompt_template = p_info["prompt_template"]
    prompt = ChatPromptTemplate.from_template(template=prompt_template)
    chain = LLMChain(llm=llm, prompt=prompt, verbose=True)
    destination_chains[name] = chain

#router chain 
destinations = [f"{p['name']}: {p['description']}" for p in prompt_information]
destinations_str = "\n".join(destinations)
router_template= MULTI_PROMPT_ROUTER_TEMPLATE.format(destinations=destinations_str)
router_prompt = PromptTemplate(
    template=router_template,
    input_variables=["input"],
    output_parser=RouterOutputParser()
)
router_chain = LLMRouterChain.from_llm(llm,router_prompt)
conversation = MultiPromptChain(router_chain=router_chain,
                 destination_chains=destination_chains,
                 default_chain=default_chain,
                 verbose=True)


result = conversation.run("내 항공편 예정된 출발 시간을 알려주세요")
print(result)