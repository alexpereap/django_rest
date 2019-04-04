import React from 'react';
import PropTypes from 'prop-types';
import spinner from '../styles/spinner.svg';

const Movies = (props) => {
  if (props.moviesReady === false) {
    return (<img height="35px" src={spinner} alt="react" />);
  }

  return (
    <div>
      {props.movies.length > 0 ? (
        <table className="table">
          <thead className="thead-dark">
            <tr>
              <th scope="col">Name</th>
              <th scope="col">Year</th>
              <th scope="col">Director</th>
              <th scope="col">Recommended</th>
              <th scope="col">&nbsp;</th>
            </tr>
          </thead>
          <tbody>
            {props.movies.map(movie => (
              <tr key={movie.id}>
                <td className="col-3">{ movie.name }</td>
                <td className="col-2">{ movie.year }</td>
                <td className="col-3">{ movie.director }</td>
                <td className="col-1">{ movie.recommended === true ? 'yes' : 'no' }</td>
                <td>
                  <a href={`/movie/${movie.id}`} className="btn btn-info">edit</a>&nbsp;
                  <a href="#" className="btn btn-danger" onClick={(e) => props.delete(e, movie.id)}>delete</a>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      )
        : (<p>There are no movies</p>)}
    </div>
  );
};

Movies.propTypes = {
  movies: PropTypes.array.isRequired,
  moviesReady: PropTypes.bool.isRequired,
  delete: PropTypes.func.isRequired,
};

export default Movies;
