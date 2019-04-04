import React from 'react';
import Movies from './Movies';
import spinner from '../styles/spinner.svg';

const API_USER = 'alexp';
const API_PASS = 'McLaren.Mp4';
const base64 = require('base-64');

class MovieApp extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      movies: [],
      movies_recommended: [],
      movies_loading: true,
      movies_recommended_loading: true,
      deleting: false,
    };
  }

  componentDidMount() {
    // request for movies
    fetch('/api/movies/', {
      headers: {
        Authorization: `Basic ${base64.encode(`${API_USER}:${API_PASS}`)}`,
      },
      credentials: 'omit',
    }).then(response => response.json())
      .then(json => {
        this.setState({ movies: json.movies, movies_loading: false });
      }).catch(error => {
        alert(error);
      });

    // request for recommended
    fetch('/api/movies/?recommended', {
      headers: {
        Authorization: `Basic ${base64.encode(`${API_USER}:${API_PASS}`)}`,
      },
      credentials: 'omit',
    }).then(response => response.json())
      .then(json => {
        this.setState({ movies_recommended: json.movies, movies_recommended_loading: false });
      }).catch(error => {
        alert(error);
      });
  }

  deleteMovie = (e, movieID) => {
    e.preventDefault();
    if (confirm('You sure?')) {
      this.setState({ deleting: true });

      fetch(`/api/movies/${movieID}`, {
        headers: {
          Authorization: `Basic ${base64.encode(`${API_USER}:${API_PASS}`)}`,
        },
        method: 'DELETE',
        credentials: 'omit',
      }).then(response => response.json())
        .then(json => {
        // remove from frontend
          const newMovies = this.state.movies.filter(movie => {
            if (movie.id !== movieID) return movie;
          });

          const newRecommendedMovies = this.state.movies_recommended.filter(movie => {
            if (movie.id !== movieID) return movie;
          });

          this.setState({ movies: newMovies, movies_recommended: newRecommendedMovies });
          this.setState({ deleting: false });
        }).catch(error => {
          this.setState({ deleting: false });
          console.log(error);
        });
    }
  };

  render() {
    return (
      <div>
        {this.state.deleting === true ? (<img height="35px" src={spinner} alt="react" />) : ('')}
        <h1>Movies</h1>
        <Movies moviesReady={!this.state.movies_loading} movies={this.state.movies} delete={this.deleteMovie} />
        <h1>Recommended Movies</h1>
        <Movies moviesReady={!this.state.movies_recommended_loading} movies={this.state.movies_recommended} delete={this.deleteMovie} />
      </div>
    );
  }
}

export default MovieApp;
