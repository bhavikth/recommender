package edu.umn.cs.recsys.uu;

import it.unimi.dsi.fastutil.longs.LongList;
import it.unimi.dsi.fastutil.longs.LongSet;

import org.grouplens.lenskit.basic.AbstractItemScorer;
import org.grouplens.lenskit.collections.CollectionUtils;
import org.grouplens.lenskit.data.dao.ItemEventDAO;
import org.grouplens.lenskit.data.dao.UserEventDAO;
import org.grouplens.lenskit.data.event.Rating;
import org.grouplens.lenskit.data.history.History;
import org.grouplens.lenskit.data.history.RatingVectorUserHistorySummarizer;
import org.grouplens.lenskit.data.history.UserHistory;
import org.grouplens.lenskit.vectors.MutableSparseVector;
import org.grouplens.lenskit.vectors.SparseVector;
import org.grouplens.lenskit.vectors.VectorEntry;
import org.grouplens.lenskit.vectors.similarity.CosineVectorSimilarity;

import javax.annotation.Nonnull;
import javax.inject.Inject;

/**
 * User-user item scorer.
 * @author <a href="http://www.grouplens.org">GroupLens Research</a>
 */
public class SimpleUserUserItemScorer extends AbstractItemScorer {
    private final UserEventDAO userDao;
    private final ItemEventDAO itemDao;

    @Inject
    public SimpleUserUserItemScorer(UserEventDAO udao, ItemEventDAO idao) {
        userDao = udao;
        itemDao = idao;
    }

    @Override
    public void score(long user, @Nonnull MutableSparseVector scores) {
        MutableSparseVector userVector = getUserRatingVector(user).mutableCopy();
        double mu = userVector.mean();
        for (VectorEntry e:userVector.fast()) {
        	userVector.set(e.getKey(),e.getValue()-mu);
        }
        // TODO Score items for this user using user-user collaborative filtering
        
        // This is the loop structure to iterate over items to score
        for (VectorEntry e: scores.fast(VectorEntry.State.EITHER)) {
        	long item = e.getKey();
        	LongSet neighbors = itemDao.getUsersForItem(item);
        	MutableSparseVector simVector = MutableSparseVector.create(neighbors);
        	for (long v:neighbors) {
        		if (v == user) {
        			continue;
        		}
        		MutableSparseVector vVector = getUserRatingVector(v).mutableCopy();
        		double mv = vVector.mean();
        		for (VectorEntry ve:vVector.fast()) {
        			vVector.set(ve.getKey(),ve.getValue()-mv);
        		}
        		simVector.set(v,new CosineVectorSimilarity().similarity(userVector, vVector));
        	}
        	LongList Nui = simVector.keysByValue(true).subList(0, 30);
        	double pui = 0;
        	double s_sum = 0;
        	for (long v:Nui) {
        		double rvi = getUserRatingVector(v).get(item);
        		double mv = getUserRatingVector(v).mean();
        		double suv = simVector.get(v);
        		pui += suv*(rvi-mv);
        		s_sum += Math.abs(suv);
        	}
        	pui = (pui/s_sum)+mu;
        	scores.set(item,pui);
        }        
        
    }

    /**
     * Get a user's rating vector.
     * @param user The user ID.
     * @return The rating vector.
     */
    private SparseVector getUserRatingVector(long user) {
        UserHistory<Rating> history = userDao.getEventsForUser(user, Rating.class);
        if (history == null) {
            history = History.forUser(user);
        }
        return RatingVectorUserHistorySummarizer.makeRatingVector(history);
    }
}
