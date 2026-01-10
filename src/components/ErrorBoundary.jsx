import { Component } from 'react';

export class ErrorBoundary extends Component {
  constructor(props) {
    super(props);
    this.state = { hasError: false, error: null };
  }

  static getDerivedStateFromError(error) {
    return { hasError: true, error };
  }

  componentDidCatch(error, errorInfo) {
    console.error('ErrorBoundary caught an error:', error, errorInfo);
  }

  handleReset = () => {
    try {
      localStorage.clear();
    } catch (e) {
      console.error('Clear storage error:', e);
    }
    window.location.reload();
  };

  render() {
    if (this.state.hasError) {
      return (
        <div className="h-screen flex flex-col items-center justify-center bg-red-900 text-white p-8 text-center">
          <h1 className="text-3xl font-bold mb-4">⚠️ 錯誤</h1>
          <p className="text-gray-300 mb-6">
            {this.state.error?.message || '發生未預期的錯誤'}
          </p>
          <button
            onClick={this.handleReset}
            className="bg-white text-red-900 px-6 py-3 rounded-xl font-bold hover:bg-gray-200 active:scale-95 transition-colors"
          >
            重置應用
          </button>
        </div>
      );
    }

    return this.props.children;
  }
}
