import ChatPageLayout from './ChatPageLayout';
import AnomalyWatchdogChat from '../components/chat/AnomalyWatchdogChat';

const AnomalyWatchdogPage = () => {
  const category = {
    id: 'anomaly-watchdog',
    title: 'Anomaly Watchdog',
    description: 'Detect unusual transactions and patterns'
  };

  return (
    <ChatPageLayout category={category}>
      {(props) => <AnomalyWatchdogChat {...props} />}
    </ChatPageLayout>
  );
};

export default AnomalyWatchdogPage;

