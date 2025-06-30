import React from 'react';
import PropTypes from 'prop-types';
import './CommentSection.css';

function CommentSection({ comments, currentUser, onDelete }) {
  if (!comments) {
    return <p>Loading comments...</p>;
  }

  return (
    <div className="comment-section">
      <h3>Comments</h3>
      {comments.length === 0 ? (
        <p>No comments yet. Be the first!</p>
      ) : (
        comments.map((comment) => (
          <div key={comment.id} className="comment">
            <p>
              <strong>{comment.user?.username || "Anonymous"}:</strong>{' '}
              {comment.content}
            </p>
            <p>Rating: {comment.rating}/5</p>
            {comment.created_at && (
              <p className="timestamp">
                <small>
                  Posted on {new Date(comment.created_at).toLocaleString()}
                </small>
              </p>
            )}
            {currentUser?.id === comment.user?.id && (
              <button
                className="delete-btn"
                onClick={() => onDelete(comment.id)}
              >
                Delete
              </button>
            )}

          </div>
        ))
      )}
    </div>
  );
}

CommentSection.propTypes = {
  comments: PropTypes.arrayOf(
    PropTypes.shape({
      id: PropTypes.number.isRequired,
      content: PropTypes.string.isRequired,
      rating: PropTypes.number.isRequired,
      user: PropTypes.shape({
        username: PropTypes.string,
      }),
      user_id: PropTypes.number,
      created_at: PropTypes.string,
    })
  ).isRequired,
  currentUser: PropTypes.shape({
    id: PropTypes.number.isRequired,
  }),
  onDelete: PropTypes.func,
};

CommentSection.defaultProps = {
  currentUser: null,
  onDelete: () => {},
};

export default CommentSection;
