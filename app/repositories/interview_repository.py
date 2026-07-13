from app.database.database import db
from bson import ObjectId # type: ignore
from datetime import datetime
from bson.errors import InvalidId # type: ignore
from fastapi import HTTPException # type: ignore

async def save_interview_session(
    session: dict
):

    result = await db.interview_sessions.insert_one(
        session
    )
    
    return result.inserted_id


async def get_interview_session(
    interview_id: str
):

    try:

        object_id = ObjectId(interview_id)

    except InvalidId:

        raise HTTPException(

            status_code=400,

            detail="Invalid interview ID."

        )

    return await db.interview_sessions.find_one(

        {
            "_id": object_id
        }

    )


async def update_interview_session(

    interview_id: str,

    data: dict

):

    return await db.interview_sessions.update_one(

        {

            "_id": ObjectId(interview_id)

        },

        {

            "$set": data

        }

    )
    
async def append_question(

    interview_id: str,

    question: dict

):

    return await db.interview_sessions.update_one(

        {

            "_id": ObjectId(interview_id)

        },

        {

            "$push": {

                "questions": question

            }

        }

    )
    
async def save_answer(

    interview_id: str,

    question_number: int,

    answer: str

):

    return await db.interview_sessions.update_one(

        {

            "_id": ObjectId(interview_id)

        },

        {

            "$set": {

                f"questions.{question_number-1}.answer": answer

            }

        }

    )
    
async def save_evaluation(

    interview_id: str,

    question_number: int,

    evaluation: dict

):

    return await db.interview_sessions.update_one(

        {

            "_id": ObjectId(interview_id)

        },

        {

            "$set": {

                f"questions.{question_number-1}.evaluation": evaluation

            }

        }

    )
    
    
async def save_report(

    interview_id: str,

    report: dict

):

    return await db.interview_sessions.update_one(

        {

            "_id": ObjectId(interview_id)

        },

        {

            "$set": {

                "report": report,

                "completed": True,

                "status": "completed"

            }

        }

    )
    
async def get_interviews_by_user(
    user_id: str
):
    cursor = db.interview_sessions.find(
        {
            "user_id": user_id
        }
    ).sort(
        "created_at",
        -1
    )

    return await cursor.to_list(length=None)

async def delete_interview(
    interview_id: str
):
    return await db.interview_sessions.delete_one(
        {
            "_id": ObjectId(interview_id)
        }
    )
    
    