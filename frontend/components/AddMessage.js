import React from 'react'
import PropTypes from 'prop-types'

const AddMessage = ({ addMessage }) => {
  let input

  return (
    <section id="new-message">
      <input
        onKeyPress={(e) => {
          if (e.key === 'Enter') {
            addMessage(input.value)
            input.value = ''
          }
        }}
        type="text"
        ref={(node) => {input = node}}
      />
    </section>
  )
}

AddMessage.propTypes = {
  addMessage: PropTypes.func.isRequired
}

export default AddMessage