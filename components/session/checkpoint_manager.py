from pymongo import MongoClient
from pymongo.server_api import ServerApi
from common import log
from typing import Dict, List
from data_types import Message
import os


class CheckpointManager(object):
    """
    Manage all middle results for each checkpoint. Store everything in MongoDB.
    """

    COLLECTION_NAME = 'checkpoints'
    MSG_LIST_FIELD = 'msg_list'

    def __init__(self):
        log.debug("[CheckpointManager] initialized")
        self.client = MongoClient(os.getenv('MONGODB_URI'), server_api=ServerApi('1'))
        self.db = self.client[os.getenv('MONGODB_DB_NAME')]
        self.collection = self.db[self.COLLECTION_NAME]

    def remove_checkpoint(self, checkpoint_id: str) -> None:
        self.collection.delete_one({'_id': checkpoint_id})
        log.info(
            f'[CheckpointManager] remove_checkpoint: checkpoint_id: {checkpoint_id}')

    def get_content(self, checkpoint_id: str, key: str) -> str:
        checkpoint = self.collection.find_one({'_id': checkpoint_id}, {key: 1})

        # if key not in checkpoint:
        if not checkpoint or key not in checkpoint:
            content = ''
            self.save_content(checkpoint_id, key, content)
        else:
            content = checkpoint[key]
        log.info(
            f'[CheckpointManager] get_content: checkpoint_id: {checkpoint_id}, key: {key}, content: {content}')
        return content

    def save_content(self, checkpoint_id: str, key: str, content: str) -> None:
        self.collection.update_one(
            {'_id': checkpoint_id},
            {'$set': {key: content}},
            upsert=True
        )
        log.info(
            f'[CheckpointManager] save_content: checkpoint_id: {checkpoint_id}, key: {key}, content: {content}')

    def get_msg_list(self, checkpoint_id: str) -> List[Dict]:
        checkpoint = self.collection.find_one(
            {'_id': checkpoint_id}, {self.MSG_LIST_FIELD: 1})

        # if self.MSG_LIST_FIELD not in checkpoint:
        if not checkpoint or self.MSG_LIST_FIELD not in checkpoint:
            msg_list = []
        else:
            msg_list = checkpoint[self.MSG_LIST_FIELD]
        log.info(
            f'[CheckpointManager] get_msg_list: checkpoint_id: {checkpoint_id}, msg_list: {msg_list}')
        return msg_list

    def add_msg(self, checkpoint_id: str, msg: Dict) -> None:
        self.collection.update_one(
            {'_id': checkpoint_id},
            {'$push': {self.MSG_LIST_FIELD: msg}},
            upsert=True
        )
        log.info(
            f'[CheckpointManager] add_msg: checkpoint_id: {checkpoint_id}, msg: {msg}')
