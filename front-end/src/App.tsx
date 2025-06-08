import React from 'react';
import ChatContainer from './components/ChatContainer';

function App() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-[#17408B] to-[#C8102E] flex items-center justify-center p-4 font-[system-ui]">
      <div className="w-full max-w-md h-[600px] md:h-[700px] rounded-xl overflow-hidden shadow-2xl">
        <ChatContainer />
      </div>
    </div>
  );
}

export default App;