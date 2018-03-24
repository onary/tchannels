import { connect } from 'react-redux'
import { bindActionCreators } from 'redux'
import AddMessageComponent from '../components/AddMessage'
import { addMessage } from '../actions'

const mapDispatchToProps = dispatch => bindActionCreators({ addMessage }, dispatch);

export const AddMessage = connect(() => ({}), mapDispatchToProps)(AddMessageComponent)
