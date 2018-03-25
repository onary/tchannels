
import * as types from '../constants/ActionTypes'
import { messageReceived, populateUsersList } from '../actions'

const setupSocket = (dispatch) => {
  const url = 'ws://' + window.location.host + '/ws/chat/'
  const socket = new WebSocket(url) // 'ws://localhost:8000/ws/chat/'

  socket.onmessage = (event) => {
    const data = JSON.parse(event.data)
    switch (data.type) {
      case types.ADD_MESSAGE:
        dispatch(messageReceived(data.message, data.author))
        break
      case types.USERS_LIST:
        dispatch(populateUsersList(data.users))
        break
      case types.ADD_MESSAGES:
        data.messages.forEach((i) => {
          dispatch(messageReceived(i.message, i.author))
        })
        break
      default:
        break
    }
  }

  return socket
}

export default setupSocket