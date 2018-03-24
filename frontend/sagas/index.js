import { takeEvery } from 'redux-saga/effects'
import * as types from '../constants/ActionTypes'

export default function* handleMessage(params) {
  yield takeEvery(types.ADD_MESSAGE, (action) => {
    params.socket.send(JSON.stringify(action))
  })
}