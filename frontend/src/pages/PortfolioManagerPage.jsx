import ChatPageLayout from './ChatPageLayout';
import PortfolioManagerChat from '../components/chat/PortfolioManagerChat';

const PortfolioManagerPage = () => {
  const category = {
    id: 'portfolio-manager',
    title: 'Portfolio Manager',
    description: 'Track and optimize your investment portfolio'
  };

  return (
    <ChatPageLayout category={category}>
      {(props) => <PortfolioManagerChat {...props} />}
    </ChatPageLayout>
  );
};

export default PortfolioManagerPage;

